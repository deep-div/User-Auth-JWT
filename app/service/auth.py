from sqlalchemy.orm import Session
from jose import JWTError
from app.service.schema import UserRegister
from app.db.read import (
    get_user_by_identifier,
)
from app.db.write import (
    create_user,
    update_password,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.schema import User
from app.service.utils import validate_registration_data, validate_login_data


def register_user(db: Session, user_data: UserRegister):
    """Handles user registration logic"""
    email, phone, password = validate_registration_data(db, user_data)

    password_hash = hash_password(password)

    user = create_user(
        db=db,
        email=email,
        phone=phone,
        password_hash=password_hash
    )

    return user


def login_user(db: Session, identifier: str, password: str):
    """Handles login authentication"""
    identifier, password = validate_login_data(identifier, password)

    user = get_user_by_identifier(db, identifier)

    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return access_token, refresh_token


def get_user_from_token(db: Session, token: str, expected_type: str = "access"):
    """Validate token and return user."""
    try:
        payload = decode_token(token)
    except JWTError:
        raise ValueError("Invalid or expired token")

    token_type = payload.get("type")
    if token_type != expected_type:
        raise ValueError(f"Expected a {expected_type} token")

    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Invalid token payload")

    try:
        parsed_user_id = int(user_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid token payload")

    user = db.query(User).filter(User.id == parsed_user_id).first()
    if not user:
        raise ValueError("User not found")

    return user


def refresh_user_tokens(db: Session, refresh_token: str):
    """Issue new access and refresh tokens using a refresh token."""
    user = get_user_from_token(db, refresh_token, expected_type="refresh")
    access_token = create_access_token({"sub": str(user.id)})
    new_refresh_token = create_refresh_token({"sub": str(user.id)})
    return access_token, new_refresh_token


def logout_user():
    """JWT logout is client-side unless token blacklist is implemented."""
    return {"success": True, "message": "Logged out successfully"}


def change_user_password(db: Session, token: str, old_password: str, new_password: str):
    """Change password for the authenticated user."""
    normalized_old = old_password.strip() if old_password else ""
    normalized_new = new_password.strip() if new_password else ""

    if not normalized_old:
        raise ValueError("Old password cannot be empty")

    if not normalized_new:
        raise ValueError("New password cannot be empty")

    if normalized_old == normalized_new:
        raise ValueError("New password must be different from old password")

    user = get_user_from_token(db, token, expected_type="access")
    if not verify_password(normalized_old, user.password_hash):
        raise ValueError("Old password is incorrect")

    new_password_hash = hash_password(normalized_new)
    update_password(db, user, new_password_hash)
    return {"success": True, "message": "Password changed successfully"}
