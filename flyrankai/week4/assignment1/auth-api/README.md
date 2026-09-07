# FlyRank Auth API

A FastAPI authentication API using Supabase Auth with JWT-based protected routes.

## Features

- User signup
- User login
- Supabase authentication
- JWT token verification
- Protected user endpoint
- Authentication dependency
- Logout endpoint
- Swagger Bearer authentication

## Tech Stack

- Python
- FastAPI
- Supabase
- JWT
- Uvicorn

## Project Structure

```text
auth-api/
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
Setup
1. Create virtual environment
python -m venv venv
2. Activate virtual environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret

Do not commit .env to GitHub.

Run the API
uvicorn main:app --reload

API documentation:

http://127.0.0.1:8000/docs
API Endpoints
Method	Endpoint	Description
GET	/	API status
GET	/public/info	Public endpoint
POST	/auth/signup	Create a new user
POST	/auth/login	Login and receive JWT
GET	/protected/me	Protected user endpoint
POST	/auth/logout	Logout
Testing
Signup

Use:

{
  "email": "your-test-email@example.com",
  "password": "your-test-password"
}
Login

Login using the registered account and obtain the access_token.

Protected Route

In Swagger, click Authorize, enter the Bearer token, and access:

GET /protected/me

A valid token returns 200 OK.

Without a valid token, the API returns 401 Unauthorized.

Invalid Token

Using an invalid or expired token should return:

{
  "detail": "Invalid or expired token"
}
Security Notes
Supabase handles user authentication.
JWT tokens are verified before accessing protected routes.
.env is excluded from Git using .gitignore.
Supabase credentials and JWT secrets must not be committed to GitHub.
Protected endpoints require Bearer authentication.

Author
Thillai Eswari T