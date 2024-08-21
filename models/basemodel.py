#!/usr/bin/python3
"""The BaseModel Module"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from typing import Dict, List, TypeVar
from uuid import uuid4


Base = declarative_base()


class BaseModel:
    """The BaseModel class"""
    __abstract__ = True
    id = Column(String(50), primary_key=True, nullable=False)
    time_created = Column(DateTime, default=datetime.now, nullable=False)
    time_updated = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initializing the Basemodel class"""
        if 'id' not in kwargs:
            self.id = str(uuid4())
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == 'time_created' or key == 'time_updated':
                    setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.time_created = datetime.now()
            self.time_updated = datetime.now()
    

    