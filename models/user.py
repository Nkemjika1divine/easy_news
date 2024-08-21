#!/usr/bin/python3
"""The User module"""
from bcrypt import hashpw, checkpw, gensalt
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class User(BaseModel, Base):
    """The User model"""
    __tablename__ = "users"
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(250), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    def hash_password(self, password: str = None) -> str:
        """Hashes a user's password"""
        if not password or type(password) is not str:
            return None
        return hashpw(password.encode("utf8"), gensalt())
    

    def is_valid_password(self, password: str = None) -> bool:
        """Verifies to ensure that password entered is the same in the DB"""
        if not password or type(password) is not str:
            return False
        if self.password is None:
            return False
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))