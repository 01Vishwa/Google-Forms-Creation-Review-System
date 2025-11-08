# 🎯 Google Forms Creation & Review System

A full-stack survey management system with Google Forms integration, approval workflows, and email notifications.

## ✨ Features

- ✅ **Survey Creation** - Upload questions or enter manually
- ✅ **Approval Workflow** - Review and approve surveys
- ✅ **Email Notifications** - Automatic emails on approval
- ✅ **Google Forms Integration** - Optional OAuth setup
- ✅ **Status Transitions** - Enforced workflow rules
- ✅ **Authentication** - Google OAuth 2.0
- ✅ **Full Testing** - 23/23 tests passing

## 🚀 Quick Start

### Windows
```cmd
scripts\setup.bat    # First time only
scripts\start.bat    # Start both servers
```

### Linux/Mac
```bash
chmod +x scripts/*.sh
./scripts/setup.sh   # First time only
./scripts/start.sh   # Start both servers
```

### Access
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📚 Documentation

All documentation is in the `docs/` folder:
- **[docs/SETUP.md](docs/SETUP.md)** - Complete setup guide
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and fixes
- **[docs/GOOGLE_FORMS_SETUP.md](docs/GOOGLE_FORMS_SETUP.md)** - Optional OAuth setup
- **[docs/README.md](docs/README.md)** - Documentation index

## 📁 Project Structure

```
├── app/              # Next.js pages
├── components/       # React components
├── backend/          # FastAPI backend
├── scripts/          # All automation scripts
├── docs/             # Documentation
└── services/         # API clients
```

## 🧪 Testing

```cmd
scripts\test.bat      # Windows
./scripts/test.sh     # Linux/Mac
```

## 🔧 Known Issues

### Google FedCM Console Warnings (Non-Critical)
You may see these warnings:
- `[GSI_LOGGER]: FedCM get() rejects with AbortError`

**These are harmless warnings** and don't affect functionality. Error suppression is implemented in `app/error-suppression.tsx`.
