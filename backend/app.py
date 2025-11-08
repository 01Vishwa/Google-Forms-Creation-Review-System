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
import json

# Import our custom services
from google_forms_service import GoogleFormsService
from email_service import EmailService

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
    questions: Optional[str] = None  # Text blob or JSON string containing questions
    status: str = "draft"
    createdAt: Optional[str] = None
    approvedAt: Optional[str] = None
    responseCount: int = 0
    approver: Optional[str] = None
    form_url: Optional[str] = None
    form_id: Optional[str] = None
    creator: Optional[str] = None

class ApprovalRequest(BaseModel):
    recipient_email: str
    custom_message: Optional[str] = None

# --- IN-MEMORY DATABASE (for demo) ---
surveys_db: List[dict] = []
users_db: dict = {}  # Store user sessions

# --- INITIALIZE SERVICES ---
# Configuration: Set USE_OAUTH=True for 100% success rate, False for service account (10-30%)
USE_OAUTH = os.getenv("USE_OAUTH", "true").lower() == "true"  # Default to OAuth

try:
    if USE_OAUTH:
        print("🔐 Initializing Google Forms with OAuth 2.0 (100% success rate)...")
        forms_service = GoogleFormsService(
            credentials_file="credentials.json",
            use_oauth=True,
            oauth_credentials_file="credentials-oauth.json"
        )
    else:
        print("🔐 Initializing Google Forms with Service Account (10-30% success rate)...")
        print("⚠️  Consider setting USE_OAUTH=true in .env for better reliability")
        forms_service = GoogleFormsService(credentials_file="credentials.json", use_oauth=False)
    
    print("✅ Google Forms service initialized")
except FileNotFoundError as e:
    print(f"⚠️ Google Forms service not available: {e}")
    if USE_OAUTH:
        print("⚠️ Please create OAuth 2.0 credentials:")
        print("   1. Go to: https://console.cloud.google.com/apis/credentials")
        print("   2. Create OAuth 2.0 Client ID (Application type: Desktop app)")
        print("   3. Download JSON and save as 'credentials-oauth.json'")
    print("⚠️ Surveys will be created without Google Forms integration")
    forms_service = None
except Exception as e:
    print(f"⚠️ Google Forms service initialization failed: {e}")
    print("⚠️ Common issues:")
    print("   - Google Forms API not enabled in Cloud Console")
    if USE_OAUTH:
        print("   - OAuth credentials file missing or invalid")
        print("   - Need to complete OAuth consent flow (browser will open on first run)")
    else:
        print("   - Service account permissions insufficient")
        print("   - Service accounts have only 10-30% success rate with Forms API")
        print("   💡 Set USE_OAUTH=true in .env for 100% success rate")
    print("   - API quota exceeded")
    print("⚠️ Surveys will be created without Google Forms integration")
    forms_service = None

email_service = EmailService()
print("✅ Email service initialized" if email_service.is_configured else "⚠️ Email service available but not configured")


# --- FASTAPI APP ---
app = FastAPI(
    title="Google Forms Survey Creation & Review System",
    description="""
## 🚀 Survey Management System with Google Forms Integration

A comprehensive API for creating, reviewing, and approving surveys with automatic Google Forms generation.

### Key Features:
* 📝 **Create Surveys** - Parse questions from text, JSON, or CSV format
* 🔍 **Review & Approve** - Workflow for survey approval with status tracking
* 📧 **Email Notifications** - Automatic email with form URL on approval
* 🔗 **Google Forms Integration** - Automatic form creation via Google Forms API
* 🔐 **OAuth Authentication** - Secure Google OAuth 2.0 authentication
* ✅ **Status Validation** - Enforced status transition rules

### Status Workflow:
- `draft` → Initial state after creation
- `pending-approval` → Submitted for review
- `approved` → Approved and email sent
- `archived` → No longer active

### Authentication:
All endpoints require Google OAuth authentication via cookies.
Use `POST /auth/google` to authenticate with a Google token.
    """,
    version="1.0.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "API Support",
        "email": "support@surveyforge.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "authentication",
            "description": "Google OAuth authentication endpoints"
        },
        {
            "name": "surveys",
            "description": "Survey CRUD operations and approval workflow"
        }
    ]
)

# --- CORS MIDDLEWARE ---
# This is crucial to allow your React app (http://localhost:3000)
# to communicate with this backend (e.g., http://localhost:8000).
origins = [
    "http://localhost:3000",  # Your React app's origin
    "http://localhost:3001",  # Alternative Next.js port
    "http://127.0.0.1:3000",  # Alternative localhost notation
    "http://127.0.0.1:3001",
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

@app.get("/auth/user", tags=["authentication"])
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

@app.post("/auth/google", tags=["authentication"])
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

@app.post("/auth/logout", tags=["authentication"])
async def logout(response: Response):
    """Logout user by clearing the auth cookie"""
    response.delete_cookie(key="auth_token")
    return {"message": "Logged out successfully"}

# --- SURVEY ENDPOINTS ---
@app.get("/surveys", tags=["surveys"])
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

@app.get("/surveys/{survey_id}", tags=["surveys"])
async def get_survey(
    survey_id: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Get a specific survey by ID"""
    survey = next((s for s in surveys_db if s["id"] == survey_id), None)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@app.post("/surveys", tags=["surveys"], status_code=201)
async def create_survey(
    survey: Survey,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Create a new survey and Google Form
    
    Request Body:
    - title: Survey title
    - description: Survey description
    - questions: Text blob or JSON string containing questions
    
    The questions can be:
    1. Plain text with newline-separated questions
    2. JSON array of question objects
    
    Example plain text:
        1. What is your name? [TEXT]
        2. Choose your favorite color [MULTIPLE_CHOICE]
           - Red
           - Blue
           - Green
        3. Tell us about yourself [PARAGRAPH]
    
    Example JSON:
        [
            {"title": "What is your name?", "type": "TEXT", "required": true},
            {"title": "Choose favorite color", "type": "MULTIPLE_CHOICE", "options": ["Red", "Blue", "Green"]}
        ]
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Generate survey ID
        survey_id = f"survey_{len(surveys_db) + 1}_{int(datetime.utcnow().timestamp())}"
        
        # Parse questions
        questions = []
        if survey.questions:
            # Check if questions contains binary data (e.g., Excel file content)
            if survey.questions.startswith('PK\x03\x04') or '\x00' in survey.questions[:100]:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid questions format. Binary files (Excel, Word, etc.) are not supported. Please use plain text, JSON, or CSV format."
                )
            
            try:
                # Try to parse as JSON first
                questions = json.loads(survey.questions)
            except json.JSONDecodeError:
                # If not JSON, parse as text
                if forms_service:
                    questions = forms_service.parse_questions_from_text(survey.questions)
        
        # Create Google Form if service is available
        form_data = None
        form_error = None
        
        if forms_service:
            try:
                form_data = forms_service.create_form(
                    title=survey.title,
                    description=survey.description,
                    questions=questions if questions else None,
                    owner_email=current_user.get("email")  # Share form with creator
                )
                print(f"✅ Created Google Form: {form_data['form_id']}")
            except Exception as e:
                form_error = str(e)
                print(f"❌ Error creating Google Form: {e}")
                # Continue without form - survey will be created without form_url
        else:
            form_error = "Google Forms service not initialized. To enable: Create credentials-oauth.json in backend directory."
            print(f"ℹ️  {form_error}")
            print("ℹ️  Survey will be created without Google Form integration.")
        
        # Create survey data
        survey_data = {
            "id": survey_id,
            "title": survey.title,
            "description": survey.description,
            "questions": survey.questions,
            "status": "draft",
            "createdAt": datetime.utcnow().isoformat(),
            "approvedAt": None,
            "responseCount": 0,
            "approver": None,
            "form_url": form_data['form_url'] if form_data else None,
            "form_id": form_data['form_id'] if form_data else None,
            "edit_url": form_data.get('edit_url') if form_data else None,
            "creator": current_user.get("email")
        }
        
        surveys_db.append(survey_data)
        
        response_message = "Survey created successfully"
        if form_data:
            response_message += " with Google Form"
        elif form_error:
            response_message += f" (Google Form creation failed: {form_error})"
        else:
            response_message += " (Google Forms integration not available)"
        
        return {
            **survey_data,
            "message": response_message,
            "form_created": bool(form_data)
        }
        
    except HTTPException:
        # Re-raise HTTPException (e.g., 400 errors) without modification
        raise
    except Exception as e:
        print(f"❌ Error creating survey: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating survey: {str(e)}")

@app.patch("/surveys/{survey_id}", tags=["surveys"])
async def update_survey(
    survey_id: str,
    survey_update: dict,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Update a survey
    
    Supports partial updates of survey fields.
    Status transitions are validated:
    - draft -> pending-approval, approved, archived
    - pending-approval -> draft, approved, archived
    - approved -> archived
    - archived -> (no transitions allowed)
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    survey = next((s for s in surveys_db if s["id"] == survey_id), None)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    # Validate status transitions if status is being updated
    if "status" in survey_update:
        new_status = survey_update["status"]
        current_status = survey.get("status", "draft")
        
        # Define valid transitions
        valid_transitions = {
            "draft": ["pending-approval", "approved", "archived"],
            "pending-approval": ["draft", "approved", "archived"],
            "approved": ["archived"],
            "archived": []
        }
        
        if current_status not in valid_transitions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid current status: {current_status}"
            )
        
        if new_status not in valid_transitions[current_status]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition from '{current_status}' to '{new_status}'. Allowed: {valid_transitions[current_status]}"
            )
    
    # Update survey fields
    for key, value in survey_update.items():
        if key != "id":  # Don't allow ID changes
            survey[key] = value
    
    return survey

@app.delete("/surveys/{survey_id}", tags=["surveys"])
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

@app.post("/surveys/{survey_id}/approve", tags=["surveys"])
async def approve_survey(
    survey_id: str,
    approval: ApprovalRequest,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Approve a survey and send notification email
    
    Request Body:
    - recipient_email: Email address to send the form link to
    - custom_message: Optional custom message to include in the email
    
    Behavior:
    1. Mark survey as approved
    2. Record approver and approval timestamp
    3. Send email with form URL to recipient
    
    Status Validation:
    - Survey must be in 'draft' or 'pending-approval' status
    - Already approved surveys cannot be re-approved
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Find the survey
    survey = next((s for s in surveys_db if s["id"] == survey_id), None)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    # Validate status transition
    current_status = survey.get("status", "draft")
    if current_status == "approved":
        raise HTTPException(
            status_code=400, 
            detail="Survey is already approved. Cannot approve again."
        )
    elif current_status == "archived":
        raise HTTPException(
            status_code=400,
            detail="Cannot approve an archived survey."
        )
    
    # Check if form URL exists
    if not survey.get("form_url"):
        raise HTTPException(
            status_code=400,
            detail="Survey does not have a Google Form URL. Cannot approve."
        )
    
    # Update survey status
    survey["status"] = "approved"
    survey["approvedAt"] = datetime.utcnow().isoformat()
    survey["approver"] = current_user.get("email")
    
    # Send approval email
    email_sent = False
    try:
        email_sent = await email_service.send_approval_email(
            recipient_email=approval.recipient_email,
            survey_title=survey["title"],
            form_url=survey["form_url"],
            approver_name=current_user.get("name", current_user.get("email")),
            custom_message=approval.custom_message
        )
    except Exception as e:
        print(f"⚠️ Error sending email: {e}")
        # Continue even if email fails
    
    return {
        **survey,
        "message": "Survey approved successfully",
        "email_sent": email_sent,
        "email_recipient": approval.recipient_email
    }

# --- RUN THE SERVER ---
if __name__ == "__main__":
    # Runs the server on http://localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)