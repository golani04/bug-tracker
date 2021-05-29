from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from backend.db import Base
from backend.utils.auth import hash_password


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, default=None)
    active = Column(Boolean, default=True)

    issues = relationship("Issue", back_populates="owner")

    @classmethod
    def create_user(cls, email, username, password, fname, lname: str, /):
        return cls(
            email=email,
            username=username,
            password=hash_password(password),
            firstname=fname,
            lastname=lname,
        )
