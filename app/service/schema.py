from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserRegister(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    """Schema for user login request"""
    identifier: str
    password: str

class TokenResponse(BaseModel):
    """Schema returned after successful authentication"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Schema returned after refreshing tokens"""
    success: bool = True
    message: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ForgotPassword(BaseModel):
    """Schema for requesting password reset"""
    identifier: str


class ResetPassword(BaseModel):
    """Schema for resetting password using reset token"""
    token: str
    new_password: str


class ChangePassword(BaseModel):
    """Schema for changing password when user is authenticated"""
    old_password: str
    new_password: str


class UserResponse(BaseModel):
    """Schema returned when sending user information"""
    id: int
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class RegisterSuccessResponse(BaseModel):
    """Schema returned on successful registration"""
    success: bool = True
    message: str
    user: UserResponse


class ErrorResponse(BaseModel):
    """Schema returned on failed request"""
    success: bool = False
    message: str
    reason: str


class MessageResponse(BaseModel):
    """Generic success message schema"""
    success: bool = True
    message: str


class MeResponse(BaseModel):
    """Schema returned by /auth/me"""
    success: bool = True
    user: UserResponse
