from fastapi import Depends, HTTPException, status
from app.models.users import User
from app.dependencies.auth import get_current_user

def require_role(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        print(f"[DEBUG] User trying to access: {current_user.username}")
        print(f"[DEBUG] User role: {current_user.role}")
        print(f"[DEBUG] Allowed roles: {allowed_roles}")

        if current_user.role not in allowed_roles:
            print("[DEBUG] Access denied.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource"
            )

        print("[DEBUG] Access granted.")
        return current_user

    return role_checker
