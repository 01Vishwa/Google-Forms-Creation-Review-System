# 🔧 Google Forms API Troubleshooting Guide

## ✅ Recent Improvements (Fixed!)

The following improvements have been implemented to prevent the 500 error:

1. **Fixed Permissions**: Changed form permission from `writer` to `reader` - now anyone with the link can view and respond
2. **Auto-Share with Creator**: Forms are now automatically shared with the creator's email address
3. **Forms Appear in Drive**: Created forms now appear in your Google Drive for easy management

---

## Issue: Google Forms API 500 Internal Error

If you're seeing this error:
```
❌ An error occurred creating the form: <HttpError 500 when requesting https://forms.googleapis.com/v1/forms?alt=json returned "Internal error">
```

This means the Google Forms API is returning an internal server error. Here's how to fix it:

---

## ✅ Solution Steps

### 1. Enable Google Forms API in Cloud Console

The Google Forms API may not be enabled for your project:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project: **forms-creation-and-review-sys**
3. Navigate to **APIs & Services** → **Library**
4. Search for "**Google Forms API**"
5. Click on it and press **"ENABLE"**

Also enable these required APIs:
- **Google Drive API** (required for form permissions)
- **Google Sheets API** (optional, for responses)

### 2. Verify Service Account Permissions

Your service account needs proper IAM permissions:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **IAM & Admin** → **Service Accounts**
3. Find: `form-creation-and-review-syste@forms-creation-and-review-sys.iam.gserviceaccount.com`
4. Make sure it has these roles:
   - **Editor** or **Owner** (for full access)
   - **Service Account User**

### 3. Check API Quotas

The API may have hit quota limits:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **Dashboard**
3. Click on **Google Forms API**
4. Check the **Quotas** tab
5. Look for:
   - **Queries per day**: Should have room left
   - **Queries per 100 seconds**: Should not be exceeded

### 4. Wait and Retry

Sometimes Google APIs have temporary issues:

- **Wait 5-10 minutes** and try again
- The error might be on Google's side and will resolve itself
- Check [Google Cloud Status Dashboard](https://status.cloud.google.com/)

### 5. Test with Google's API Explorer

Verify the API works directly:

1. Go to [Google Forms API Explorer](https://developers.google.com/forms/api/reference/rest/v1/forms/create)
2. Try creating a test form
3. If it fails here too, the issue is with Google's API or your project setup

---

## 🔄 Alternative: Use OAuth Instead of Service Account

If service account continues to fail, you can use OAuth2 user credentials:

### Update `.env`:
```properties
# Set to 'true' to use OAuth2 user credentials
USE_OAUTH=true
```

### Run OAuth Flow:
```python
# This will open a browser for you to authorize
python backend/google_forms_service.py
```

---

## 🛠️ Temporary Workaround

The system will continue to work **without** Google Forms integration:

1. **Surveys are still created** in the database
2. **Approval flow still works**
3. **Email notifications still send**
4. You just won't get automatic Google Form creation

To use this mode, simply continue - the backend handles it gracefully.

---

## 📋 Verify Your Setup

Run this to check if the API is accessible:

```cmd
cd backend
python -c "from googleapiclient.discovery import build; from google.oauth2 import service_account; creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/forms.body']); service = build('forms', 'v1', credentials=creds); print('✅ API accessible')"
```

If this works, the issue is with the specific form creation request.
If this fails, the issue is with your credentials or API access.

---

## 🆘 Still Having Issues?

### Check These Common Problems:

1. **Project Billing**: Make sure billing is enabled in Google Cloud Console
2. **API Restrictions**: Check if there are API key restrictions
3. **Service Account Key**: Try generating a new service account key
4. **Region Issues**: Some APIs have regional availability

### Get More Details:

Enable debug logging in the backend:

```python
# Add to backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show more detailed error messages.

---

## ✅ Quick Fix Summary

**Most Common Solution:**
1. Enable Google Forms API in Cloud Console
2. Enable Google Drive API in Cloud Console
3. Wait 5 minutes for changes to propagate
4. Restart the backend server
5. Try creating a survey again

**If that doesn't work:**
- The system will still function without Google Forms
- You can manually create forms and add the URLs
- Focus on other features while troubleshooting

---

## 📞 Need Help?

Check these resources:
- [Google Forms API Documentation](https://developers.google.com/forms/api)
- [Service Account Setup Guide](https://cloud.google.com/iam/docs/service-accounts)
- [API Error Troubleshooting](https://cloud.google.com/apis/docs/troubleshooting-api-errors)
