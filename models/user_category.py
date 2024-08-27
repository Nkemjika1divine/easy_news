#!/usr/bin/python3
"""The User_Category module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class User_Category(BaseModel, Base):
    """The User_Category Model"""
    __tablename__ = "user_categories"
    user_id = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    category_id = Column(String(50), ForeignKey("categories.id", ondelete='CASCADE'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)