#!/usr/bin/python3
"""The News module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class News(BaseModel, Base):
    """The News Model"""
    __tablename__ = "news"
    channel_id = Column(String(50), ForeignKey("channels.id", ondelete='CASCADE'), nullable=False)
    headline = Column(String(500), nullable=False)
    description = Column(String(1000), nullable=True)
    category_id = Column(String(50), ForeignKey("categories.id", ondelete='CASCADE'), nullable=False)
    url = Column(String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)