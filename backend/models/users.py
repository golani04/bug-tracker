from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.models.base import BaseModel
from backend.utils.auth import hash_password


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)

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
