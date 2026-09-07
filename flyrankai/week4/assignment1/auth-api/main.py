import os
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from jose import jwt

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="FlyRank Auth API",
    version="1.0.0"
)
security = HTTPBearer()
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
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
@app.get("/protected/me")
def protected_me(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Protected route accessed",
        "user": current_user
    }
@app.post("/auth/logout")
def logout():
    try:
        supabase.auth.sign_out()
        return {
            "message": "Logout successful"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )