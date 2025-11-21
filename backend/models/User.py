from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from .Base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    accounts = relationship("Account", back_populates="user")
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"