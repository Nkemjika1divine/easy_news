#!/usr/bin/python3
"""Module for Authentication"""
from fastapi import Request
from models.session import Session
from typing import TypeVar


class Auth():
    """Auth class for handling authentication"""

    def create_session(self, user_id: str = None) -> str:
        """Creaates a session ID for a user"""
        from models import storage
        if user_id is None or type(user_id) is not str:
            return None
        user = storage.search_key_value("User", "id", user_id)
        if user:
            session = Session()
            session.user_id = user_id
            session.save()
            return session.id
        return None