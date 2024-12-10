# Factory Management System - API Security

This is my implementation of the Factory Management System with JWT token authentication and role-based access control.

## What I Learned
- How to implement JWT token authentication
- Password hashing for security
- Role-based access control
- API security best practices
- How to protect sensitive routes

## Setup Instructions

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Testing the API

1. Register a new user:
```bash
curl -X POST http://localhost:5003/register -H "Content-Type: application/json" -d '{"username": "testuser", "password": "TestPass123!"}'
```

2. Login:
```bash
curl -X POST http://localhost:5003/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "TestPass123!"}'
```

3. Access protected route (replace TOKEN with your token):
```bash
curl http://localhost:5003/profile -H "Authorization: Bearer TOKEN"
```

## Security Features
- Password must be at least 8 characters
- Must include uppercase, lowercase, numbers, and special characters
- JWT tokens expire after 24 hours
- Rate limiting to prevent brute force attacks
- Role-based access control for admin routes
