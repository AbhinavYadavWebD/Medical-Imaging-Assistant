from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth, patients, reports, images, ai
from app.database.init_db import init_db
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import os
from app.routers import annotations
# ✅ Load environment variables from .env
load_dotenv()

# ✅ Create the FastAPI app
app = FastAPI(title="Medical Imaging and Report Assistant")

# ✅ Enable SessionMiddleware (required for OAuth login with Authlib)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-session-key"))

# ✅ Debug log
print("CORS Middleware enabled.")

# ✅ Enable CORS before mounting routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Initialize database
init_db()

# ✅ Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(images.router, prefix="/images", tags=["Images"])
app.include_router(ai.router, prefix="/ai", tags=["AI Assistant"])
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(annotations.router, prefix="/annotations", tags=["Annotations"])

# ✅ Root route
@app.get("/")
def root():
    return {"message": "Medical Imaging Backend is running."}
