#!/bin/bash

# Python SDK Generator Script for Google Forms Survey API
# Generates a Python SDK from the OpenAPI specification

echo "🚀 Google Forms Survey API - Python SDK Generator"
echo "================================================"

# Configuration
API_URL="http://localhost:8000"
OPENAPI_URL="${API_URL}/openapi.json"
SDK_OUTPUT_DIR="./google_forms_survey_sdk"
SDK_PACKAGE_NAME="google_forms_survey_sdk"

# Check if server is running
echo "📡 Checking if backend server is running..."
if ! curl -s "${API_URL}" > /dev/null; then
    echo "❌ Backend server is not running at ${API_URL}"
    echo "Please start the server with: python app.py"
    exit 1
fi

echo "✅ Server is running"

# Install OpenAPI Generator CLI if not installed
if ! command -v openapi-generator-cli &> /dev/null; then
    echo "📦 Installing OpenAPI Generator CLI..."
    npm install -g @openapitools/openapi-generator-cli
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install OpenAPI Generator CLI"
        echo "Please install manually: npm install -g @openapitools/openapi-generator-cli"
        exit 1
    fi
fi

echo "✅ OpenAPI Generator CLI is installed"

# Remove old SDK directory if exists
if [ -d "${SDK_OUTPUT_DIR}" ]; then
    echo "🗑️  Removing old SDK directory..."
    rm -rf "${SDK_OUTPUT_DIR}"
fi

# Generate SDK
echo "🔨 Generating Python SDK from OpenAPI spec..."
echo "OpenAPI URL: ${OPENAPI_URL}"
echo "Output directory: ${SDK_OUTPUT_DIR}"

openapi-generator-cli generate \
    -i "${OPENAPI_URL}" \
    -g python \
    -o "${SDK_OUTPUT_DIR}" \
    --package-name "${SDK_PACKAGE_NAME}" \
    --additional-properties=\
packageName="${SDK_PACKAGE_NAME}",\
packageVersion="1.0.0",\
projectName="Google Forms Survey SDK",\
packageUrl="https://github.com/yourusername/google-forms-survey-sdk"

if [ $? -ne 0 ]; then
    echo "❌ Failed to generate SDK"
    exit 1
fi

echo "✅ SDK generated successfully!"

# Install SDK in development mode
echo "📦 Installing SDK in development mode..."
cd "${SDK_OUTPUT_DIR}"
pip install -e .
cd ..

echo ""
echo "✅ SDK Installation Complete!"
echo ""
echo "📚 Usage Example:"
echo "================================================"
cat << 'EOF'
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
auth_api = AuthenticationApi(client)

# Retrieve all surveys
surveys = surveys_api.get_surveys(skip=0, limit=10)
print(f"Total surveys: {surveys.total}")

# Get specific survey
survey = surveys_api.get_survey(survey_id="survey_123")
print(f"Survey: {survey.title}")

# Create new survey
new_survey = surveys_api.create_survey(
    survey={
        "title": "Customer Feedback",
        "description": "Tell us what you think",
        "questions": "1. What is your name? [TEXT]\n2. Rate us [MULTIPLE_CHOICE]\n- Excellent\n- Good\n- Average"
    }
)
print(f"Created survey: {new_survey.id}")

# Approve survey
approved = surveys_api.approve_survey(
    survey_id=new_survey.id,
    approval_request={
        "recipient_email": "user@example.com",
        "custom_message": "Please share this survey"
    }
)
print(f"Survey approved: {approved.status}")

# Delete survey
surveys_api.delete_survey(survey_id=survey.id)
print("Survey deleted")
EOF

echo ""
echo "================================================"
echo "SDK Location: ${SDK_OUTPUT_DIR}"
echo "Package Name: ${SDK_PACKAGE_NAME}"
echo ""
