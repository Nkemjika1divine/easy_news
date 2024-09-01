#!/usr/bin/python3
"""The Channel module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String


class Channel(BaseModel, Base):
    """The Channel Model"""
    __tablename__ = "channels"
    channel_name = Column(String(50), nullable=False)
    source = Column(String(50), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)