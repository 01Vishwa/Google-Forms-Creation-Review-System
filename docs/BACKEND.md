# FastAPI Backend for Survey Management System

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
copy .env.example .env
```

### 3. Run the Development Server

```bash
uvicorn app:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

## Project Structure

```
backend/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create from .env.example)
├── .env.example       # Example environment variables
└── README.md          # This file
```

## API Endpoints (To be implemented)

### Authentication
- `POST /auth/google` - Google OAuth login
- `POST /auth/logout` - Logout
- `GET /auth/user` - Get current user

### Surveys
- `GET /surveys` - List all surveys
- `GET /surveys/{id}` - Get survey by ID
- `POST /surveys` - Create new survey
- `PATCH /surveys/{id}` - Update survey
- `DELETE /surveys/{id}` - Delete survey
- `POST /surveys/{id}/approve` - Approve survey

## Technologies

- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM for database
- **Uvicorn** - ASGI server
- **Google OAuth** - Authentication
