from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import bcrypt
import os
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
load_dotenv()


from app.database.session import SessionLocal
from app.models.users import User
from app.schemas import users as user_schema
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# ---------- Database Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# ---------- OAuth Setup ----------
oauth = OAuth()
oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# ---------- GitHub OAuth Start ----------
@router.get("/oauth/github")
async def github_login(request: Request):
    redirect_uri = os.getenv("GITHUB_REDIRECT_URI")
    return await oauth.github.authorize_redirect(request, redirect_uri)

# ---------- GitHub OAuth Callback ----------
@router.get("/oauth/github/callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.get("user", token=token)
    user_info = user_info.json()

    # Fetch primary email
    email_resp = await oauth.github.get("user/emails", token=token)
    emails = email_resp.json()
    primary_email = next((e["email"] for e in emails if e["primary"]), None)

    user_data = {
        "username": user_info["login"],
        "email": primary_email or f'{user_info["login"]}@github.com',
        "role": "admin" if "github.com" in primary_email else "student"
    }

    # Check if user exists or create
    user = db.query(User).filter(User.email == user_data["email"]).first()
    if not user:
        fake_password = bcrypt.hashpw("oauth_default".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            hashed_password=fake_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    # Redirect back to frontend with token
    frontend_url = os.getenv("FRONTEND_REDIRECT_URL", "http://localhost:3000")
    redirect_url = f"{frontend_url}?token={token}&username={user.username}&email={user.email}&role={user.role}"
    return RedirectResponse(redirect_url)

# ---------- Signup ----------
@router.post("/signup", response_model=user_schema.UserOut)
def signup(users: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == users.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = get_password_hash(users.password)
    db_user = User(
        username=users.username,
        email=users.email,
        hashed_password=hashed_pw,
        role="student"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ---------- Login ----------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }
