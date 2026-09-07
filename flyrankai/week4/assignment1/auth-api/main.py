import os
from fastapi import FastAPI, HTTPException, Header
from jose import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="FlyRank Auth API",
    version="1.0.0"
)


class AuthRequest(BaseModel):
    email: str
    password: str


@app.get("/")
def root():
    return {
        "message": "FlyRank Auth API is running"
    }


@app.get("/public/info")
def public_info():
    return {
        "message": "This is a public endpoint"
    }


@app.post("/auth/signup")
def signup(request: AuthRequest):
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })

        return {
            "message": "Signup successful",
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/auth/login")
def login(request: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        if response.session is None:
            raise HTTPException(
                status_code=401,
                detail="Login failed: no session returned"
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "user": response.user
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
@app.get("/protected/me")
def protected_me(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )

        return {
            "message": "Protected route accessed",
            "user": payload
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )