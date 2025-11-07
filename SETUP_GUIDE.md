# 🚀 Installation & Setup Guide

## Backend Setup

### 1. Install Python Dependencies

First, navigate to the backend directory and install the required packages:

```cmd
cd backend
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn (API framework)
- Google Forms API & Gmail API clients
- Authentication libraries (JWT, Google OAuth)
- Email service (aiosmtplib)

### 2. Configure Environment Variables

The `.env` file has been updated with the correct Google Client ID. Make sure these settings are configured:

```properties
# Google OAuth Configuration
GOOGLE_CLIENT_ID=331931690873-9sarog6q4rjjiedp1glq35t832l5gkgj.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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

# JWT Configuration
JWT_SECRET_KEY=1nCaMObXCst877vo-5CrZPjxDbpPmP663VXWZUGLsPk
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Email SMTP Configuration (Optional - for sending approval emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Server Configuration
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

#### 📧 Email Configuration (Optional)

To enable email notifications when surveys are approved:

1. Use a Gmail account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Create an app password for "Mail"
3. Update `SMTP_USER` and `SMTP_PASSWORD` in `.env`

**Note:** Email is optional. The system will work without it, but approval emails won't be sent.

### 3. Verify Google Service Account

The `credentials.json` file contains your Google service account credentials. This enables:
- Creating Google Forms via API
- Managing form permissions
- Accessing form responses

**The credentials are already configured and ready to use!**

### 4. Start the Backend Server

```cmd
cd backend
python app.py
```

Or using uvicorn directly:

```cmd
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at: **http://localhost:8000**

---

## Frontend Setup

### 1. Install Node Dependencies

```cmd
npm install
# or
pnpm install
```

### 2. Start the Development Server

```cmd
npm run dev
# or
pnpm dev
```

The frontend will be available at: **http://localhost:3000**

---

## 🎯 Features & API Endpoints

### Backend API Endpoints

#### Authentication
- `POST /auth/google` - Authenticate with Google OAuth
- `GET /auth/user` - Get current user info
- `POST /auth/logout` - Logout user

#### Surveys
- `GET /surveys` - List all surveys (with pagination & filtering)
- `GET /surveys/{id}` - Get specific survey details
- `POST /surveys` - Create new survey with Google Form
- `PATCH /surveys/{id}` - Update survey (with status validation)
- `DELETE /surveys/{id}` - Delete survey
- `POST /surveys/{id}/approve` - Approve survey and send email

---

## 📋 Usage Flow

### 1. Create a Survey

**Via Frontend:**
1. Click "Create Survey" button
2. Choose "Manual Entry" or "Upload File"
3. Enter:
   - Survey title
   - Description
   - Questions (one per line or formatted)
4. Preview questions
5. Submit

**Supported File Formats:**
- ✅ **Plain Text (.txt)** - One question per line
- ✅ **JSON (.json)** - Structured question objects
- ✅ **CSV (.csv)** - Questions in first column
- ❌ **Excel (.xlsx, .xls)** - Not supported (convert to TXT/CSV first)

**Question Format:**
```
1. What is your name? [TEXT]
2. Choose your favorite color [MULTIPLE_CHOICE]
   - Red
   - Blue
   - Green
3. Tell us about yourself [PARAGRAPH]
```

See [QUESTION_FILE_FORMATS.md](QUESTION_FILE_FORMATS.md) for detailed formatting guide.

**Via API:**
```bash
curl -X POST http://localhost:8000/surveys \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Customer Satisfaction Survey",
    "description": "Help us improve our service",
    "questions": "1. What is your name?\n2. How satisfied are you?\n3. Any feedback?"
  }'
```

**What Happens:**
- ✅ Survey is created in the database
- ✅ Google Form is automatically created via API
- ✅ Form URL is saved with the survey
- ✅ Survey status is set to "draft"

### 2. Review & Approve Survey

**Via Frontend:**
1. Click on a survey to view details
2. Enter recipient email address
3. (Optional) Add custom message
4. Click "Approve & Send Email"

**Via API:**
```bash
curl -X POST http://localhost:8000/surveys/{survey_id}/approve \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "stakeholder@example.com",
    "custom_message": "Please share this survey with customers"
  }'
```

**What Happens:**
- ✅ Survey status changes to "approved"
- ✅ Approval timestamp and approver are recorded
- ✅ Email is sent to recipient with form link (if SMTP configured)
- ✅ Form URL is included in the email

### 3. Manage Surveys

**Status Transitions:**
- `draft` → `pending-approval`, `approved`, `archived`
- `pending-approval` → `draft`, `approved`, `archived`
- `approved` → `archived`
- `archived` → (no transitions)

**Update Survey Status:**
```bash
curl -X PATCH http://localhost:8000/surveys/{survey_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "pending-approval"}'
```

**Delete Survey:**
```bash
curl -X DELETE http://localhost:8000/surveys/{survey_id}
```

---

## 🔧 Troubleshooting

### Issue: "Token has wrong audience" Error

**Solution:** ✅ Already fixed! The `.env` file now has the correct Google Client ID that matches the frontend.

### Issue: Google Forms Not Creating

**Possible Causes:**
1. Service account credentials missing or invalid
2. Google Forms API not enabled in Google Cloud Console

**Solution:**
1. Verify `credentials.json` exists in the backend directory
2. Enable Google Forms API:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Forms API" and enable it
   - Also enable "Google Drive API"

### Issue: Emails Not Sending

**Possible Causes:**
1. SMTP credentials not configured
2. Gmail blocking "less secure apps"

**Solution:**
1. Use Gmail App Passwords (see Email Configuration above)
2. Check `SMTP_USER` and `SMTP_PASSWORD` in `.env`
3. The system will log a warning but continue working without email

### Issue: "Not authenticated" Error

**Solution:**
1. Clear browser cookies
2. Log out and log in again with Google
3. Make sure both frontend and backend are running
4. Check that CORS is properly configured

---

## 📊 Data Models

### Survey Object
```typescript
{
  id: string              // Unique survey ID
  title: string           // Survey title
  description: string     // Survey description
  questions: string       // Text blob or JSON questions
  status: "draft" | "pending-approval" | "approved" | "archived"
  createdAt: string       // ISO timestamp
  approvedAt: string      // ISO timestamp (nullable)
  responseCount: number   // Number of form responses
  approver: string        // Email of approver (nullable)
  form_url: string        // Google Form public URL
  form_id: string         // Google Form ID
  edit_url: string        // Google Form edit URL
  creator: string         // Email of creator
}
```

---

## 🎨 Frontend Components

### Key Components:
- `Dashboard` - Main survey management interface
- `CreateSurveyModal` - Survey creation form
- `SurveyDetailsModal` - View/approve survey details
- `SurveyList` - Display surveys with filtering
- `AuthContext` - Google OAuth authentication

### State Management:
- Context API for authentication
- React hooks for local state
- Axios for API communication

---

## 🔐 Security Notes

### Authentication
- Google OAuth 2.0 for user authentication
- JWT tokens stored in HTTP-only cookies
- Token expiration: 24 hours (configurable)

### CORS Configuration
- Frontend origin: `http://localhost:3000`
- Credentials enabled for cookie support
- Update in production to match your domain

### Environment Variables
- ⚠️ Never commit `.env` file to git
- Use different credentials for production
- Rotate JWT secret key regularly

---

## 🚀 Production Deployment

### Backend:
1. Set `secure=True` for cookies (requires HTTPS)
2. Update CORS origins to production domain
3. Use environment variables for secrets
4. Enable HTTPS/TLS
5. Use a production WSGI server (Gunicorn + Uvicorn)

### Frontend:
1. Build production bundle: `npm run build`
2. Update API URL to production backend
3. Configure environment variables
4. Deploy to Vercel, Netlify, or your hosting

---

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🎯 Next Steps

1. ✅ **Backend is configured** - Google Client IDs now match
2. ✅ **Google Forms integration ready** - Service account configured
3. ✅ **Email service available** - Configure SMTP for email sending
4. ⏭️ **Restart backend server** - Apply the new configuration
5. ⏭️ **Test the complete flow** - Create → Approve → Email

---

## 📞 Support

If you encounter any issues:
1. Check the console logs (both frontend and backend)
2. Verify environment variables are set correctly
3. Ensure all dependencies are installed
4. Check Google Cloud Console for API quotas/limits

---

**Happy surveying! 🎉**
