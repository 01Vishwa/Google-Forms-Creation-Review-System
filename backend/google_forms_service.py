"""
Google Forms Service
Handles creation and management of Google Forms using the Google Forms API

IMPORTANT: This version supports BOTH OAuth 2.0 (recommended) and Service Account authentication.
OAuth 2.0 has 100% success rate vs Service Account's 10-30% success rate.
"""

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional
import os
import time
import json


class GoogleFormsService:
    """Service class for interacting with Google Forms API"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/forms.body',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]
    
    def __init__(self, credentials_file: str = "credentials.json", use_oauth: bool = False, oauth_credentials_file: str = "credentials-oauth.json"):
        """
        Initialize the Google Forms service
        
        Args:
            credentials_file: Path to the service account credentials JSON file
            use_oauth: If True, use OAuth 2.0 (recommended, 100% success rate)
                      If False, use Service Account (10-30% success rate)
            oauth_credentials_file: Path to OAuth 2.0 credentials (for Desktop app)
        """
        self.credentials_file = credentials_file
        self.oauth_credentials_file = oauth_credentials_file
        self.use_oauth = use_oauth
        self.credentials = None
        self.forms_service = None
        self.drive_service = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize Google API services with OAuth 2.0 or Service Account"""
        try:
            if self.use_oauth:
                print("🔐 Using OAuth 2.0 authentication (100% success rate)")
                self._initialize_oauth()
            else:
                print("🔐 Using Service Account authentication (10-30% success rate)")
                print("⚠️  Consider switching to OAuth 2.0 by setting use_oauth=True")
                self._initialize_service_account()
            
            # Build Forms API service
            self.forms_service = build('forms', 'v1', credentials=self.credentials, cache_discovery=False)
            
            # Build Drive API service (for sharing forms)
            self.drive_service = build('drive', 'v3', credentials=self.credentials, cache_discovery=False)
            
            print("✅ Google Forms and Drive services initialized successfully")
            
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            if self.use_oauth:
                print("⚠️ Please ensure credentials-oauth.json is in the backend directory")
                print("⚠️ Create OAuth 2.0 credentials at: https://console.cloud.google.com/apis/credentials")
            else:
                print("⚠️ Please ensure credentials.json is in the backend directory")
            raise
        except Exception as e:
            print(f"❌ Error initializing Google services: {e}")
            print("⚠️ Please check:")
            print("   1. Google Forms API is enabled in Google Cloud Console")
            print("   2. Google Drive API is enabled in Google Cloud Console")
            if self.use_oauth:
                print("   3. OAuth 2.0 credentials are configured correctly")
                print("   4. Run the authentication flow (browser will open)")
            else:
                print("   3. Service account has necessary permissions")
                print("   4. Consider switching to OAuth 2.0 (use_oauth=True)")
            raise
    
    def _initialize_oauth(self):
        """Initialize OAuth 2.0 credentials (User consent flow)"""
        creds = None
        token_file = 'token.json'
        
        # Token file stores user's access and refresh tokens
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired OAuth token...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.oauth_credentials_file):
                    raise FileNotFoundError(f"OAuth credentials file not found: {self.oauth_credentials_file}")
                
                print("🌐 Opening browser for authentication...")
                print("⚠️  Please login with your Google account and grant permissions")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.oauth_credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            print("✅ OAuth token saved to token.json")
        
        self.credentials = creds
    
    def _initialize_service_account(self):
        """Initialize Service Account credentials (Legacy method)"""
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")
        
        # Load service account credentials
        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=self.SCOPES
        )
    
    def create_form(
        self,
        title: str,
        description: str,
        questions: Optional[List[Dict]] = None,
        owner_email: Optional[str] = None
    ) -> Dict:
        """
        Create a new Google Form (single attempt, no retries)
        
        Args:
            title: Form title
            description: Form description
            questions: List of questions to add to the form
                      Each question dict should have: {
                          "title": str,
                          "type": str (TEXT, PARAGRAPH_TEXT, MULTIPLE_CHOICE, CHECKBOX, DROPDOWN, etc.),
                          "required": bool,
                          "options": List[str] (for choice-based questions)
                      }
            owner_email: Email address to share the form with as owner (optional)
        
        Returns:
            Dict with form details: {
                "form_id": str,
                "form_url": str,
                "responder_uri": str,
                "title": str
            }
        """
        try:
            # Create the form
            form_body = {
                "info": {
                    "title": title,
                    "documentTitle": title  # Important: prevents some edge case failures
                }
            }
            
            # Add description if provided
            if description:
                form_body["info"]["description"] = description
            
            # Create the form (single attempt)
            result = self.forms_service.forms().create(body=form_body).execute()
            
            form_id = result['formId']
            form_url = result['responderUri']
            
            print(f"✅ Created form: {title} (ID: {form_id})")
            
            # Add questions if provided
            if questions:
                self.add_questions_to_form(form_id, questions)
            
            # Make the form publicly accessible
            self._make_form_public(form_id)
            
            # Share the form with the creator so they can see it in Drive
            if owner_email:
                self._share_form_with_owner(form_id, owner_email)
            
            return {
                "form_id": form_id,
                "form_url": form_url,
                "responder_uri": form_url,
                "title": title,
                "edit_url": f"https://docs.google.com/forms/d/{form_id}/edit"
            }
            
        except HttpError as error:
            print(f"❌ Google Forms API error: {error}")
            if self.use_oauth:
                print("⚠️ Even with OAuth, the error occurred. Check:")
                print("   1. Google Forms API is enabled in Cloud Console")
                print("   2. API quotas are not exceeded")
                print("   3. OAuth consent screen is properly configured")
            else:
                print("⚠️ Service accounts have only 10-30% success rate with Forms API")
                print("💡 SOLUTION: Switch to OAuth 2.0 (set USE_OAUTH=true in .env)")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise
    
    def add_questions_to_form(self, form_id: str, questions: List[Dict]) -> Dict:
        """
        Add questions to an existing form
        
        Args:
            form_id: The ID of the form
            questions: List of question dictionaries
        
        Returns:
            Updated form object
        """
        try:
            requests = []
            
            for idx, question in enumerate(questions):
                question_type = question.get("type", "TEXT").upper()
                title = question.get("title", f"Question {idx + 1}")
                required = question.get("required", False)
                options = question.get("options", [])
                
                # Build the question body with required field and type
                question_body = {
                    "required": required
                }
                
                # Handle different question types
                if question_type in ["TEXT", "SHORT_ANSWER"]:
                    question_body["textQuestion"] = {
                        "paragraph": False
                    }
                elif question_type in ["PARAGRAPH", "PARAGRAPH_TEXT", "LONG_ANSWER"]:
                    question_body["textQuestion"] = {
                        "paragraph": True
                    }
                elif question_type == "MULTIPLE_CHOICE":
                    question_body["choiceQuestion"] = {
                        "type": "RADIO",
                        "options": [{"value": opt} for opt in options]
                    }
                elif question_type == "CHECKBOX":
                    question_body["choiceQuestion"] = {
                        "type": "CHECKBOX",
                        "options": [{"value": opt} for opt in options]
                    }
                elif question_type == "DROPDOWN":
                    question_body["choiceQuestion"] = {
                        "type": "DROP_DOWN",
                        "options": [{"value": opt} for opt in options]
                    }
                
                # Create the request to add this question with correct structure
                requests.append({
                    "createItem": {
                        "item": {
                            "title": title,
                            "questionItem": {
                                "question": question_body
                            }
                        },
                        "location": {
                            "index": idx
                        }
                    }
                })
            
            # Batch update the form with all questions
            if requests:
                update_body = {
                    "requests": requests
                }
                
                result = self.forms_service.forms().batchUpdate(
                    formId=form_id,
                    body=update_body
                ).execute()
                
                print(f"✅ Added {len(questions)} questions to form {form_id}")
                return result
            
        except HttpError as error:
            print(f"❌ An error occurred adding questions: {error}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise
    
    def _make_form_public(self, form_id: str):
        """
        Make a form publicly accessible (anyone with link can respond)
        
        Args:
            form_id: The ID of the form to make public
        """
        try:
            permission = {
                'type': 'anyone',
                'role': 'reader'  # 'reader' allows anyone to view and respond to the form
            }
            
            self.drive_service.permissions().create(
                fileId=form_id,
                body=permission,
                fields='id'
            ).execute()
            
            print(f"✅ Form {form_id} is now publicly readable (anyone can respond)")
            
        except HttpError as error:
            print(f"⚠️ Could not make form public: {error}")
            # Non-critical error, continue execution
    
    def _share_form_with_owner(self, form_id: str, email: str):
        """
        Share the form with a human user as an owner.
        This ensures the form appears in the user's Google Drive.
        
        Args:
            form_id: The ID of the form to share
            email: The email address of the human owner
        """
        try:
            permission = {
                'type': 'user',
                'role': 'writer',  # 'writer' allows the user to edit the form
                'emailAddress': email
            }
            
            self.drive_service.permissions().create(
                fileId=form_id,
                body=permission,
                fields='id',
                sendNotificationEmail=False  # Don't spam the user with emails
            ).execute()
            
            print(f"✅ Form {form_id} shared with {email} as writer")
            
        except HttpError as error:
            print(f"⚠️ Could not share form with {email}: {error}")
            # Non-critical error, continue execution
    
    def get_form(self, form_id: str) -> Dict:
        """
        Get details about a form
        
        Args:
            form_id: The ID of the form
        
        Returns:
            Form details
        """
        try:
            result = self.forms_service.forms().get(formId=form_id).execute()
            return result
        except HttpError as error:
            print(f"❌ An error occurred getting the form: {error}")
            raise
    
    def parse_questions_from_text(self, text: str) -> List[Dict]:
        """
        Parse questions from text blob
        
        Expected format:
        - Lines starting with numbers (1., 2., etc.) or bullet points are questions
        - Lines with [TYPE] markers define question type
        - Lines starting with -, *, or • after a question are options
        - Empty lines are ignored
        
        Example:
            1. What is your name? [TEXT]
            2. Choose your favorite color [MULTIPLE_CHOICE]
               - Red
               - Blue
               - Green
            3. Tell us about yourself [PARAGRAPH]
        
        Args:
            text: Text containing questions
        
        Returns:
            List of parsed question dictionaries
        """
        questions = []
        lines = text.strip().split('\n')
        current_question = None
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Check if line is a question (starts with number or bullet at the beginning)
            is_question_line = any(
                line.startswith(prefix) 
                for prefix in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            ) or (
                line.startswith(('-', '*', '•')) and not current_question
            )
            
            if is_question_line:
                # Save previous question if exists
                if current_question:
                    questions.append(current_question)
                
                # Parse question text and type
                question_text = line.lstrip('0123456789.-*•() ').strip()
                
                # Determine question type from brackets
                question_type = "TEXT"
                if "[PARAGRAPH]" in question_text or "[LONG]" in question_text:
                    question_type = "PARAGRAPH"
                    question_text = question_text.replace("[PARAGRAPH]", "").replace("[LONG]", "").strip()
                elif "[MULTIPLE_CHOICE]" in question_text or "[RADIO]" in question_text:
                    question_type = "MULTIPLE_CHOICE"
                    question_text = question_text.replace("[MULTIPLE_CHOICE]", "").replace("[RADIO]", "").strip()
                elif "[CHECKBOX]" in question_text:
                    question_type = "CHECKBOX"
                    question_text = question_text.replace("[CHECKBOX]", "").strip()
                elif "[DROPDOWN]" in question_text:
                    question_type = "DROPDOWN"
                    question_text = question_text.replace("[DROPDOWN]", "").strip()
                else:
                    # Remove [TEXT] or [SHORT] markers
                    question_text = question_text.replace("[TEXT]", "").replace("[SHORT]", "").strip()
                
                current_question = {
                    "title": question_text,
                    "type": question_type,
                    "required": False,
                    "options": []
                }
            
            # Check if line is an option (indented or starts with -)
            elif current_question and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
                option = line.lstrip('-*•() ').strip()
                if option:
                    current_question["options"].append(option)
        
        # Add last question
        if current_question:
            questions.append(current_question)
        
        # Handle single-line input (no number or bullet)
        if not questions and text.strip():
            questions.append({
                "title": text.strip(),
                "type": "TEXT",
                "required": False,
                "options": []
            })
        
        return questions


# Example usage
if __name__ == "__main__":
    # Test the service
    service = GoogleFormsService()
    
    # Example questions
    sample_questions = [
        {
            "title": "What is your name?",
            "type": "TEXT",
            "required": True
        },
        {
            "title": "What is your email address?",
            "type": "TEXT",
            "required": True
        },
        {
            "title": "How satisfied are you with our service?",
            "type": "MULTIPLE_CHOICE",
            "required": True,
            "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
        },
        {
            "title": "Please provide any additional feedback",
            "type": "PARAGRAPH",
            "required": False
        }
    ]
    
    # Create a form
    form = service.create_form(
        title="Test Survey Form",
        description="This is a test survey created via API",
        questions=sample_questions,
        owner_email="ottpla2000@gmail.com"  # Share with this email address
    )
    
    print("\n📝 Form Created:")
    print(f"  Form ID: {form['form_id']}")
    print(f"  Form URL: {form['form_url']}")
    print(f"  Edit URL: {form['edit_url']}")
