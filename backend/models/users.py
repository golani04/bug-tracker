from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from backend.db import Base
from backend.schemas.users import UserType
from backend.utils.auth import hash_password


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(128), unique=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    role = Column(SmallInteger, nullable=False, default=int(UserType.viewer))

    created_at = Column(DateTime, default=datetime.utcnow())
    active = Column(Boolean, default=True)
