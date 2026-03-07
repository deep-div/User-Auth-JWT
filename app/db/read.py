from sqlalchemy.orm import Session
from app.db.schema import User


def get_user_by_email(db: Session, email: str):
    """Fetch user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    """Fetch user by phone"""
    return db.query(User).filter(User.phone == phone).first()


def get_user_by_identifier(db: Session, identifier: str):
    """Fetch user by email or phone"""
    return db.query(User).filter(
        (User.email == identifier) | (User.phone == identifier)
    ).first()


def get_user_by_id(db: Session, user_id: int):
    """Fetch user by id"""
    return db.query(User).filter(User.id == user_id).first()