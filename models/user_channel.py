#!/usr/bin/python3
"""The User_Channel module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class User_Channel(BaseModel, Base):
    """The User_Channel Model"""
    __tablename__ = "user_channels"
    user_id = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    channel_id = Column(String(50), ForeignKey("channels.id", ondelete='CASCADE'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)