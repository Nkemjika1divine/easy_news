"""The Follow module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Follow(BaseModel, Base):
    """The Follow Model"""
    __tablename__ = "follows"
    user_id = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    channel_id = Column(String(50), ForeignKey("channels.id", ondelete='CASCADE'), nullable=False)
    notifications = Column(String(5), nullable=True, default="off")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)