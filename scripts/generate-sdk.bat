@echo off
REM Python SDK Generator Script for Google Forms Survey API
REM Generates a Python SDK from the OpenAPI specification

echo ================================================
echo Google Forms Survey API - Python SDK Generator
echo ================================================
echo.

REM Configuration
set API_URL=http://localhost:8000
set OPENAPI_URL=%API_URL%/openapi.json
set SDK_OUTPUT_DIR=google_forms_survey_sdk
set SDK_PACKAGE_NAME=google_forms_survey_sdk

REM Check if server is running
echo Checking if backend server is running...
curl -s %API_URL% >nul 2>&1
if errorlevel 1 (
    echo ERROR: Backend server is not running at %API_URL%
    echo Please start the server with: python app.py
    exit /b 1
)
echo Server is running
echo.

REM Check if OpenAPI Generator CLI is installed
where openapi-generator-cli >nul 2>&1
if errorlevel 1 (
    echo Installing OpenAPI Generator CLI...
    call npm install -g @openapitools/openapi-generator-cli
    if errorlevel 1 (
        echo ERROR: Failed to install OpenAPI Generator CLI
        echo Please install manually: npm install -g @openapitools/openapi-generator-cli
        exit /b 1
    )
)
echo OpenAPI Generator CLI is installed
echo.

REM Remove old SDK directory if exists
if exist "%SDK_OUTPUT_DIR%" (
    echo Removing old SDK directory...
    rmdir /s /q "%SDK_OUTPUT_DIR%"
)

REM Generate SDK
echo Generating Python SDK from OpenAPI spec...
echo OpenAPI URL: %OPENAPI_URL%
echo Output directory: %SDK_OUTPUT_DIR%
echo.

openapi-generator-cli generate -i "%OPENAPI_URL%" -g python -o "%SDK_OUTPUT_DIR%" --package-name "%SDK_PACKAGE_NAME%" --additional-properties=packageName=%SDK_PACKAGE_NAME%,packageVersion=1.0.0,projectName="Google Forms Survey SDK",packageUrl="https://github.com/yourusername/google-forms-survey-sdk"

if errorlevel 1 (
    echo ERROR: Failed to generate SDK
    exit /b 1
)

echo SDK generated successfully!
echo.

REM Install SDK in development mode
echo Installing SDK in development mode...
cd "%SDK_OUTPUT_DIR%"
pip install -e .
cd ..

echo.
echo ================================================
echo SDK Installation Complete!
echo ================================================
echo.
echo Usage Example:
echo ================================================
echo from google_forms_survey_sdk import ApiClient, Configuration
echo from google_forms_survey_sdk.api.surveys_api import SurveysApi
echo.
echo # Configure API client
echo config = Configuration()
echo config.host = "http://localhost:8000"
echo.
echo # Create API client  
echo client = ApiClient(configuration=config)
echo.
echo # Initialize API instances
echo surveys_api = SurveysApi(client)
echo.
echo # Retrieve all surveys
echo surveys = surveys_api.get_surveys(skip=0, limit=10)
echo print(f"Total surveys: {surveys.total}")
echo.
echo # Create new survey
echo new_survey = surveys_api.create_survey(
echo     survey={
echo         "title": "Customer Feedback",
echo         "description": "Tell us what you think",
echo         "questions": "1. What is your name? [TEXT]"
echo     }
echo )
echo.
echo # Approve survey
echo approved = surveys_api.approve_survey(
echo     survey_id=new_survey.id,
echo     approval_request={
echo         "recipient_email": "user@example.com"
echo     }
echo )
echo.
echo ================================================
echo SDK Location: %SDK_OUTPUT_DIR%
echo Package Name: %SDK_PACKAGE_NAME%
echo ================================================
