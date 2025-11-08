# 📚 Documentation Index

Welcome to the **Google Forms Creation & Review System** documentation!

## 🚀 Quick Start

1. **[Setup Guide](SETUP.md)** - Installation and configuration
2. **[Running the System](#running-the-system)** - Start backend and frontend
3. **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions

---

## 📖 Documentation Files

### Core Documentation
- **[SETUP.md](SETUP.md)** - Complete setup instructions for backend and frontend
- **[GOOGLE_FORMS_SETUP.md](GOOGLE_FORMS_SETUP.md)** - Optional Google Forms OAuth integration
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - All error fixes and solutions

### Reference Documentation
- **[BACKEND.md](BACKEND.md)** - Backend API documentation and architecture
- **[QUESTION_FORMATS.md](QUESTION_FORMATS.md)** - Supported question file formats
- **[ANALYSIS.md](ANALYSIS.md)** - Complete code analysis and requirements verification

---

## 🚀 Running the System

### Quick Start (Windows)
```cmd
# Option 1: Use automation scripts
scripts\setup.bat      # First time only
scripts\start.bat      # Start both servers

# Option 2: Manual start
scripts\start-backend.bat     # Terminal 1
npm run dev                   # Terminal 2
```

### Quick Start (Linux/Mac)
```bash
# Option 1: Use automation scripts
chmod +x scripts/*.sh
./scripts/setup.sh     # First time only
./scripts/start.sh     # Start both servers

# Option 2: Manual start
./scripts/start-backend.sh    # Terminal 1
npm run dev                   # Terminal 2
```

### Access Points
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📁 Project Structure

```
├── app/                  # Next.js pages and routes
├── components/           # React UI components
├── backend/              # FastAPI backend
├── scripts/              # Automation scripts
├── docs/                 # Documentation (you are here)
├── services/             # API clients
├── lib/                  # Utilities
└── public/               # Static assets
```

---

## 🧪 Testing

```cmd
# Run all backend tests
scripts\test.bat      # Windows
./scripts/test.sh     # Linux/Mac

# Or manually
cd backend
pytest -v
```

---

## 🔧 Scripts Available

All scripts are located in the `scripts/` folder:

| Script | Purpose | Platform |
|--------|---------|----------|
| `setup.bat/sh` | Install all dependencies | Both |
| `start.bat/sh` | Start backend + frontend | Both |
| `test.bat/sh` | Run backend tests | Both |
| `start-backend.bat` | Start backend only | Windows |
| `generate-sdk.py` | Generate Python SDK | Both |

---

## 📞 Need Help?

1. Check **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for common issues
2. Review **[SETUP.md](SETUP.md)** for configuration
3. See **[GOOGLE_FORMS_SETUP.md](GOOGLE_FORMS_SETUP.md)** for OAuth setup

---

## 🎯 Feature Status

| Feature | Status | Documentation |
|---------|--------|---------------|
| Survey Creation | ✅ Working | [BACKEND.md](BACKEND.md) |
| Approval Workflow | ✅ Working | [BACKEND.md](BACKEND.md) |
| Email Notifications | ✅ Working | [SETUP.md](SETUP.md) |
| Google Forms Integration | 🟡 Optional | [GOOGLE_FORMS_SETUP.md](GOOGLE_FORMS_SETUP.md) |
| Authentication | ✅ Working | [SETUP.md](SETUP.md) |
| Status Transitions | ✅ Working | [ANALYSIS.md](ANALYSIS.md) |

---

**Last Updated:** November 8, 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
