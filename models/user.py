#!/usr/bin/python3
"""The User module"""
from bcrypt import hashpw, checkpw, gensalt
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String
from utils.utility import generate_token


class User(BaseModel, Base):
    """The User model"""
    __tablename__ = "users"
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    reset_token = Column(String(50), nullable=True)
    role = Column(String(10), nullable=False)
    email_verified = Column(String(10), nullable=False, default="no")

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
    

    def generate_password_token(self, user_id: str = None) -> str:
        """Generated a password token using uuid"""
        from models import storage
        if not user_id or type(user_id) is not str:
            return None
        user = storage.search_key_value("User", "id", user_id)
        if not user:
            raise ValueError()
        token = generate_token()
        user[0].reset_token = token
        storage.save()
        return token
    

    def update_password(self, token: str = None, password: str = None) -> None:
        """Updates a user's password"""
        from models import storage
        user = storage.search_key_value("User", "reset_token", token)
        if not user:
            raise ValueError()
        user = user[0]
        user.password = self.hash_password(password)
        user.reset_token = None
        storage.save()