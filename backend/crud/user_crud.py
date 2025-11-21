from backend.db import get_db
from backend.models.User import User
from sqlalchemy.orm import Session

def create_user(db: Session, username: str, email: str, password_hash: str):
    user = User(username=username, email=email, password_hash=password_hash)
    db.add(user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        return True
    return False

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()