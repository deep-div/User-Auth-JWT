from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.service.schema import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterSuccessResponse,
    ErrorResponse,
    ChangePassword,
    MessageResponse,
    MeResponse,
)
from app.service.auth import (
    register_user,
    login_user,
    refresh_user_tokens,
    logout_user,
    change_user_password,
    get_user_from_token,
)
from app.db.session import get_db
from shared.logger import logger

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer(auto_error=False)


@router.get("/health")
def health_check():
    """Returns service health status"""
    return {"status": "ok"}


@router.post("/register", response_model=RegisterSuccessResponse, responses={400: {"model": ErrorResponse}})
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """API endpoint for registering a new user"""

    try:
        user = register_user(db, user_data)
        logger.info("Register success")
        return {
            "success": True,
            "message": "User registered successfully",
            "user": user,
        }
    except ValueError as e:
        logger.warning(f"Register failed: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Registration failed",
                "reason": str(e),
            },
        )


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """API endpoint for user login"""

    try:
        access_token, refresh_token = login_user(db, user_data.identifier, user_data.password)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        logger.warning(f"Login failed: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh", response_model=RefreshTokenResponse, responses={401: {"model": ErrorResponse}})
def refresh_tokens(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Issue fresh access/refresh tokens from refresh token."""
    try:
        access_token, refresh_token = refresh_user_tokens(db, payload.refresh_token)
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except ValueError as e:
        logger.warning(f"Refresh failed: {str(e)}")
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Token refresh failed",
                "reason": str(e),
            },
        )


@router.post("/logout", response_model=MessageResponse, responses={401: {"model": ErrorResponse}})
def logout(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """Logout endpoint for client-side token removal."""
    if credentials is None or not credentials.credentials:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Logout failed",
                "reason": "Authorization token is required",
            },
        )
    return logout_user()


@router.post("/change-password", response_model=MessageResponse, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}})
def change_password(
    payload: ChangePassword,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    """Change password for the authenticated user."""
    if credentials is None or not credentials.credentials:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Password change failed",
                "reason": "Authorization token is required",
            },
        )
    try:
        return change_user_password(db, credentials.credentials, payload.old_password, payload.new_password)
    except ValueError as e:
        logger.warning(f"Change password failed: {str(e)}")
        status_code = 401 if "token" in str(e).lower() else 400
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": "Password change failed",
                "reason": str(e),
            },
        )


@router.get("/me", response_model=MeResponse, responses={401: {"model": ErrorResponse}})
def me(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    """Get current authenticated user details."""
    if credentials is None or not credentials.credentials:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Fetch profile failed",
                "reason": "Authorization token is required",
            },
        )
    try:
        user = get_user_from_token(db, credentials.credentials, expected_type="access")
        return {"success": True, "user": user}
    except ValueError as e:
        logger.warning(f"Get profile failed: {str(e)}")
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Fetch profile failed",
                "reason": str(e),
            },
        )
