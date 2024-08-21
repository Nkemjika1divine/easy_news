#!/usr/bin/python3
"""The User module"""
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