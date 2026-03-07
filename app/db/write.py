from sqlalchemy.orm import Session
from app.db.schema import User


def create_user(db: Session, email: str, phone: str, password_hash: str):
    """Create new user in database"""
    user = User(
        email=email,
        phone=phone,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_password(db: Session, user: User, new_password_hash: str):
    """Update user password"""
    user.password_hash = new_password_hash
    db.commit()
    db.refresh(user)
    return user