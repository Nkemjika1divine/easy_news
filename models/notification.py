#!/usr/bin/python3
"""The Notification module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Notification(BaseModel, Base):
    """The Notification Model"""
    __tablename__ = "notifications"
    user_id = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    channel_id = Column(String(50), ForeignKey("channels.id", ondelete='CASCADE'), nullable=False)
    article_title = Column(String(500), nullable=False)
    article_description = Column(String(1000), nullable=True)
    article_url = Column(String(200), nullable=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)