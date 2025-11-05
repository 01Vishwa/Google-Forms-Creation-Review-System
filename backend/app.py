# FastAPI Application
import uvicorn
from fastapi import FastAPI, HTTPException, Body, Query, Depends, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "331931690873-9sarog6q4rjjiedp1glq35t832l5gkgj.apps.googleusercontent.com")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# --- DATA MODELS ---
# This model defines the expected data from your React frontend
class GoogleToken(BaseModel):
    token: str

class Survey(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    status: str = "draft"
    createdAt: Optional[str] = None
    approvedAt: Optional[str] = None
    responseCount: int = 0
    approver: Optional[str] = None
    form_url: Optional[str] = None

class ApprovalRequest(BaseModel):
    recipient_email: str
    custom_message: Optional[str] = None

# --- IN-MEMORY DATABASE (for demo) ---
surveys_db: List[dict] = []
users_db: dict = {}  # Store user sessions

# --- FASTAPI APP ---
app = FastAPI()

# --- CORS MIDDLEWARE ---
# This is crucial to allow your React app (http://localhost:3000)
# to communicate with this backend (e.g., http://localhost:8000).
origins = [
    "http://localhost:3000",  # Your React app's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],
)

# --- HELPER FUNCTIONS ---
def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except PyJWTError:
        return None

async def get_current_user(auth_token: Optional[str] = Cookie(None)):
    """Dependency to get current authenticated user"""
    if not auth_token:
        return None
    
    user_data = verify_token(auth_token)
    if not user_data:
        return None
    
    return user_data

# --- API ENDPOINTS ---
@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.get("/auth/user")
async def get_current_user_info(current_user: Optional[dict] = Depends(get_current_user)):
    """
    Returns the current authenticated user's information.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {
        "email": current_user.get("email"),
        "name": current_user.get("name"),
        "picture": current_user.get("picture")
    }

@app.post("/auth/google")
async def verify_google_token(body: GoogleToken, response: Response):
    """
    Receives the Google ID Token from the frontend,
    verifies it, and returns the user's information with JWT token.
    """
    try:
        # Verify the ID token using Google's library
        id_info = id_token.verify_oauth2_token(
            body.token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )

        # Token is valid. `id_info` contains the user's profile data.
        user_email = id_info.get("email")
        user_name = id_info.get("name")
        user_picture = id_info.get("picture")
        
        print(f"User verified: {user_email}")

        # Create JWT token for our app
        token_data = {
            "email": user_email,
            "name": user_name,
            "picture": user_picture
        }
        access_token = create_access_token(token_data)
        
        # Set HTTP-only cookie with the token
        response.set_cookie(
            key="auth_token",
            value=access_token,
            httponly=True,
            max_age=JWT_EXPIRATION_HOURS * 3600,
            samesite="lax",
            secure=False  # Set to True in production with HTTPS
        )

        # Store user in memory (in production, use database)
        users_db[user_email] = token_data

        return {
            "message": "Login successful",
            "user": {
                "email": user_email,
                "name": user_name,
                "picture": user_picture
            }
        }

    except ValueError as e:
        # This error fires if the token is invalid
        print(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=401, 
            detail="Invalid Google token"
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error"
        )

@app.post("/auth/logout")
async def logout(response: Response):
    """Logout user by clearing the auth cookie"""
    response.delete_cookie(key="auth_token")
    return {"message": "Logged out successfully"}

# --- SURVEY ENDPOINTS ---
@app.get("/surveys")
async def get_surveys(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=1000),
    status: Optional[str] = None,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get all surveys with pagination and optional status filter
    """
    # Filter surveys by status if provided
    filtered_surveys = surveys_db
    if status and status != "all":
        filtered_surveys = [s for s in surveys_db if s.get("status") == status]
    
    # Apply pagination
    paginated_surveys = filtered_surveys[skip:skip + limit]
    
    return {
        "surveys": paginated_surveys,
        "total": len(filtered_surveys),
        "skip": skip,
        "limit": limit
    }

@app.get("/surveys/{survey_id}")
async def get_survey(
    survey_id: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Get a specific survey by ID"""
    survey = next((s for s in surveys_db if s["id"] == survey_id), None)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@app.post("/surveys")
async def create_survey(
    survey: Survey,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Create a new survey"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Generate survey ID
    survey_id = f"survey_{len(surveys_db) + 1}_{datetime.utcnow().timestamp()}"
    
    survey_data = {
        "id": survey_id,
        "title": survey.title,
        "description": survey.description,
        "status": "draft",
        "createdAt": datetime.utcnow().isoformat(),
        "approvedAt": None,
        "responseCount": 0,
        "approver": None,
        "form_url": survey.form_url,
        "creator": current_user.get("email")
    }
    
    surveys_db.append(survey_data)
    return survey_data

@app.patch("/surveys/{survey_id}")
async def update_survey(
    survey_id: str,
    survey_update: dict,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Update a survey"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    survey = next((s for s in surveys_db if s["id"] == survey_id), None)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    # Update survey fields
    for key, value in survey_update.items():
        if key != "id":  # Don't allow ID changes
            survey[key] = value
    
    return survey

@app.delete("/surveys/{survey_id}")
async def delete_survey(
    survey_id: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Delete a survey"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    survey = next((s for s in surveys_db if s["id"] == survey_id), None)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    surveys_db.remove(survey)
    return {"message": "Survey deleted successfully"}

@app.post("/surveys/{survey_id}/approve")
async def approve_survey(
    survey_id: str,
    approval: ApprovalRequest,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Approve a survey"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    survey = next((s for s in surveys_db if s["id"] == survey_id), None)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    survey["status"] = "approved"
    survey["approvedAt"] = datetime.utcnow().isoformat()
    survey["approver"] = current_user.get("email")
    
    return survey

# --- RUN THE SERVER ---
if __name__ == "__main__":
    # Runs the server on http://localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)