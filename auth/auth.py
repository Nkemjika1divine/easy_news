#!/usr/bin/python3
"""Module for Authentication"""
from fastapi import Request
from models.session import Session
from typing import Dict, TypeVar


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
    

    def get_user_id_using_session_id(self, session_id: str = None) -> str:
        """Returns a user based on Session ID"""
        from models import storage
        if session_id is None or type(session_id) is not str:
            return None
        session = storage.search_key_value("Session", "id", session_id)
        if session:
            return session[0].user_id
        return None

    
    async def get_request_header(self, request: Request) -> Dict:
        """Accesses header in the user's request"""
        if request:
            return request.headers
        else:
            return {}