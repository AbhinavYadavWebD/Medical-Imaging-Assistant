from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserOut, UserRoleUpdate
from app.dependencies.auth import get_current_active_admin
from app.database.init_db import init_db
from app.models.reports import Report
from app.models.patients import Patient


router = APIRouter(prefix="/admin", tags=["Admin"])

# ✅ Get All Users (Admin only)
@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(init_db), admin: User = Depends(get_current_active_admin)):
    users = db.query(User).all()
    return [UserOut.model_validate(u) for u in users]


# ✅ Get User by ID (Admin only)
@router.get("/users/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(init_db),
    current_admin: User = Depends(get_current_active_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ✅ Update Role
@router.put("/users/{user_id}/role", response_model=UserOut)
def update_user_role(
    user_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(init_db),
    current_admin: User = Depends(get_current_active_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user

# ✅ Delete User
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(init_db),
    current_admin: User = Depends(get_current_active_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# ✅ Dashboard Summary with Real Stats
# ✅ Dashboard Summary with Extended Stats
@router.get("/dashboard")
def get_admin_dashboard(
    db: Session = Depends(init_db),
    current_admin: User = Depends(get_current_active_admin)
):
    total_users = db.query(User).count()
    total_admins = db.query(User).filter(User.role == "admin").count()
    total_students = db.query(User).filter(User.role == "student").count()
    total_instructors = db.query(User).filter(User.role == "instructor").count()

    total_patients = db.query(Patient).count()
    total_reports = db.query(Report).count()

    latest_user = (
        db.query(User)
        .order_by(User.created_at.desc())
        .first()
    )

    return {
        "message": f"Welcome Admin {current_admin.username}",
        "stats": {
            "total_users": total_users,
            "total_admins": total_admins,
            "total_students": total_students,
            "total_instructors": total_instructors,
            "total_patients": total_patients,
            "total_reports": total_reports,
            "latest_user_joined": {
                "username": latest_user.username,
                "created_at": latest_user.created_at
            } if latest_user else None
        }
    }


