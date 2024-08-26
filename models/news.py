#!/usr/bin/python3
"""The Channel module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String


class News(BaseModel, Base):
    """The Channel Model"""
    __tablename__ = "channels"
    headline = Column(String(500), nullable=False)
    description = Column(String(1000), nullable=True)
    category_id = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)