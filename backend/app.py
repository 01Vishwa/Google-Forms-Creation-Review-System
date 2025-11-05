# FastAPI Application
import uvicorn
from fastapi import FastAPI 
import os 
import time 
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

# --- CONFIGURATION ---
# Paste your Client ID here.
# You get this from the "OAuth client created" pop-up.
GOOGLE_CLIENT_ID = "331931690873-9sarog6q4rjiedp1glq35t832l5gkgj.apps.googleusercontent.com"

# --- DATA MODELS ---
# This model defines the expected data from your React frontend
class GoogleToken(BaseModel):
    token: str

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

# --- API ENDPOINTS ---
@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.get("/auth/user")
async def get_current_user():
    """
    Returns the current authenticated user's information.
    In a production app, you would verify the session/JWT token here.
    """
    # For now, returning a mock response since we don't have session management
    # You should implement proper session/JWT token verification here
    return {
        "user": None,
        "message": "No active session. Please log in."
    }

@app.post("/auth/google")
async def verify_google_token(body: GoogleToken):
    """
    Receives the Google ID Token from the frontend,
    verifies it, and returns the user's information.
    """
    try:
        # Verify the ID token using Google's library
        # This checks if the token is valid, not expired,
        # and was issued to YOUR client ID.
        id_info = id_token.verify_oauth2_token(
            body.token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )

        # Token is valid. `id_info` contains the user's profile data.
        user_email = id_info.get("email")
        user_name = id_info.get("name")
        
        print(f"User verified: {user_email}")

        # Here, you would typically:
        # 1. Check if the user exists in your database.
        # 2. If not, create a new user record.
        # 3. Create a session or your own JWT token for your app.
        # 4. Return that session token to the frontend.

        # For this example, we'll just return the user's info
        return {
            "message": "Login successful",
            "user": {
                "email": user_email,
                "name": user_name
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

# --- RUN THE SERVER ---
if __name__ == "__main__":
    # Runs the server on http://localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)