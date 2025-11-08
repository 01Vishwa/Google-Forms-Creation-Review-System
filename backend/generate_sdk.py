"""
Python SDK Generator for Google Forms Survey API
Generates a Python SDK from the OpenAPI specification using OpenAPI Generator CLI
"""

import subprocess
import sys
import os
import requests
import json
import shutil

# Configuration
API_URL = "http://localhost:8000"
OPENAPI_URL = f"{API_URL}/openapi.json"
SDK_OUTPUT_DIR = "google_forms_survey_sdk"
SDK_PACKAGE_NAME = "google_forms_survey_sdk"

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

def check_server_running():
    """Check if the backend server is running"""
    print(f"📡 Checking if backend server is running at {API_URL}...")
    try:
        response = requests.get(API_URL, timeout=5)
        print("✅ Server is running\n")
        return True
    except requests.exceptions.RequestException:
        print(f"❌ Backend server is not running at {API_URL}")
        print("Please start the server with: python app.py")
        return False

def check_openapi_generator():
    """Check if OpenAPI Generator CLI is installed"""
    print("📦 Checking OpenAPI Generator CLI...")
    try:
        result = subprocess.run(
            ["openapi-generator-cli", "version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print("✅ OpenAPI Generator CLI is installed\n")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  OpenAPI Generator CLI not found")
    print("Installing via npm...")
    try:
        subprocess.run(
            ["npm", "install", "-g", "@openapitools/openapi-generator-cli"],
            check=True
        )
        print("✅ OpenAPI Generator CLI installed\n")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Failed to install OpenAPI Generator CLI")
        print("Please install manually:")
        print("  npm install -g @openapitools/openapi-generator-cli")
        return False

def remove_old_sdk():
    """Remove old SDK directory if exists"""
    if os.path.exists(SDK_OUTPUT_DIR):
        print(f"🗑️  Removing old SDK directory: {SDK_OUTPUT_DIR}")
        shutil.rmtree(SDK_OUTPUT_DIR)
        print("✅ Old SDK removed\n")

def generate_sdk():
    """Generate Python SDK using OpenAPI Generator"""
    print("🔨 Generating Python SDK from OpenAPI spec...")
    print(f"OpenAPI URL: {OPENAPI_URL}")
    print(f"Output directory: {SDK_OUTPUT_DIR}\n")
    
    command = [
        "openapi-generator-cli",
        "generate",
        "-i", OPENAPI_URL,
        "-g", "python",
        "-o", SDK_OUTPUT_DIR,
        "--package-name", SDK_PACKAGE_NAME,
        "--additional-properties",
        f"packageName={SDK_PACKAGE_NAME},"
        f"packageVersion=1.0.0,"
        f'projectName=Google Forms Survey SDK,'
        f"packageUrl=https://github.com/yourusername/google-forms-survey-sdk"
    ]
    
    try:
        subprocess.run(command, check=True)
        print("\n✅ SDK generated successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to generate SDK: {e}\n")
        return False

def install_sdk():
    """Install SDK in development mode"""
    print("📦 Installing SDK in development mode...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", SDK_OUTPUT_DIR],
            check=True
        )
        print("✅ SDK installed successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install SDK: {e}\n")
        return False

def print_usage_example():
    """Print SDK usage example"""
    print_header("SDK Installation Complete! 🎉")
    
    print("📚 Usage Example:")
    print("=" * 60)
    
    example_code = '''
from google_forms_survey_sdk import ApiClient, Configuration
from google_forms_survey_sdk.api.surveys_api import SurveysApi
from google_forms_survey_sdk.api.authentication_api import AuthenticationApi

# Configure API client
config = Configuration()
config.host = "http://localhost:8000"

# Create API client
client = ApiClient(configuration=config)

# Initialize API instances
surveys_api = SurveysApi(client)

# 1. Retrieve all surveys
surveys_response = surveys_api.get_surveys(skip=0, limit=10)
print(f"Total surveys: {surveys_response['total']}")
print(f"Surveys: {len(surveys_response['surveys'])}")

# 2. Get specific survey by ID
survey = surveys_api.get_survey(survey_id="survey_123")
print(f"Survey title: {survey['title']}")
print(f"Status: {survey['status']}")

# 3. Create new survey
new_survey = surveys_api.create_survey(
    survey={
        "title": "Customer Feedback Survey",
        "description": "We value your feedback",
        "questions": """
1. What is your name? [TEXT]
2. Rate our service [MULTIPLE_CHOICE]
   - Excellent
   - Good
   - Average
   - Poor
3. Any additional comments? [PARAGRAPH]
"""
    }
)
print(f"Created survey ID: {new_survey['id']}")
print(f"Form URL: {new_survey.get('form_url')}")

# 4. Update survey
updated = surveys_api.update_survey(
    survey_id=new_survey['id'],
    body={"status": "pending-approval"}
)
print(f"Updated status: {updated['status']}")

# 5. Approve survey and send email
approved = surveys_api.approve_survey(
    survey_id=new_survey['id'],
    approval_request={
        "recipient_email": "stakeholder@example.com",
        "custom_message": "Please share this survey with your team"
    }
)
print(f"Survey approved: {approved['status']}")
print(f"Email sent to: {approved['email_recipient']}")

# 6. List surveys with filtering
draft_surveys = surveys_api.get_surveys(skip=0, limit=100, status="draft")
print(f"Draft surveys: {len(draft_surveys['surveys'])}")

# 7. Delete survey (when needed)
surveys_api.delete_survey(survey_id=survey['id'])
print("Survey deleted successfully")
'''
    
    print(example_code)
    print("=" * 60)
    print(f"\n📁 SDK Location: {SDK_OUTPUT_DIR}/")
    print(f"📦 Package Name: {SDK_PACKAGE_NAME}")
    print(f"🌐 API URL: {API_URL}")
    print(f"📖 OpenAPI Spec: {OPENAPI_URL}")
    print("\n✨ You can now import and use the SDK in your Python projects!")
    print()

def main():
    """Main execution function"""
    print_header("Google Forms Survey API - Python SDK Generator")
    
    # Step 1: Check if server is running
    if not check_server_running():
        sys.exit(1)
    
    # Step 2: Check OpenAPI Generator CLI
    if not check_openapi_generator():
        sys.exit(1)
    
    # Step 3: Remove old SDK
    remove_old_sdk()
    
    # Step 4: Generate SDK
    if not generate_sdk():
        sys.exit(1)
    
    # Step 5: Install SDK
    if not install_sdk():
        sys.exit(1)
    
    # Step 6: Print usage instructions
    print_usage_example()
    
    print("🎉 SDK generation and installation complete!")
    print("Happy coding! 🚀\n")

if __name__ == "__main__":
    main()
