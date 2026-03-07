import re
from sqlalchemy.orm import Session

from app.service.schema import UserRegister
from app.db.read import get_user_by_email, get_user_by_phone


def validate_registration_data(db: Session, user_data: UserRegister) -> tuple[str | None, str | None, str]:
    """Validate registration payload and return normalized values."""
    email = user_data.email.strip() if user_data.email else None
    phone = user_data.phone.strip() if user_data.phone else None
    password = user_data.password.strip() if user_data.password else ""

    if not password:
        raise ValueError("Password cannot be empty")

    if user_data.email is not None and not email:
        raise ValueError("Email cannot be empty")

    if user_data.phone is not None and not phone:
        raise ValueError("Phone cannot be empty")

    if not email and not phone:
        raise ValueError("Email or phone is required")

    if email and phone:
        raise ValueError("Provide either email or phone, not both")

    if email:
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

        existing = get_user_by_email(db, email)
        if existing:
            raise ValueError("Email already registered")

    if phone:
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(phone) != 10:
            raise ValueError("Phone number must be 10 digits")

        existing = get_user_by_phone(db, phone)
        if existing:
            raise ValueError("Phone already registered")

    return email, phone, password


def validate_login_data(identifier: str, password: str) -> tuple[str, str]:
    """Validate login payload and return normalized values."""
    normalized_identifier = identifier.strip() if identifier else ""
    normalized_password = password.strip() if password else ""

    if not normalized_identifier:
        raise ValueError("Identifier cannot be empty")

    if not normalized_password:
        raise ValueError("Password cannot be empty")

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if "@" in normalized_identifier:
        if not re.match(email_pattern, normalized_identifier):
            raise ValueError("Invalid email format")
    elif normalized_identifier.isdigit():
        if len(normalized_identifier) != 10:
            raise ValueError("Phone number must be 10 digits")
    else:
        raise ValueError("Identifier must be a valid email or 10-digit phone number")

    return normalized_identifier, normalized_password
