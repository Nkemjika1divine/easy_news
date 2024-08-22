#!/usr/bin/python3
"""Module for Authentication"""
from fastapi import Request
from models.session import Session
from os import environ
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
        
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.
        -   If path is in excluded_paths, it does not require authentication"""
        if path is None:
            return True
        if not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        else:
            path_with_slash = path + '/'
            if path_with_slash in excluded_paths:
                return False
            else:
                for paths in excluded_paths:
                    if paths[-1] == '*':
                        count = 0
                        for i in paths:
                            count += 1
                            if path[0:count - 1] == paths[0:-1]:
                                return False
                return True
    

    async def get_authorization_header(self, request: Request) -> str:
        """Retrieves the authorization header from a request"""
        headers = await self.get_request_header(request)
        return headers.get("Authorization", None)
    

    def session_cookie(self, request: Request):
        """Returns a session id from a request's cookie"""
        if not request:
            return None
        my_session_id = environ.get("SESSION_NAME", None)
        return request.cookies.get(my_session_id)
    

    def check_for_current_user(self, request: Request) -> TypeVar("User"):
        """Checks if a request is from a current user in the database and returns the user"""
        from models import storage
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        session = storage.search_key_value("Session", "id", session_id)
        if not session:
            return None
        user = storage.search_key_value("User", "id", session[0].user_id)
        if not user:
            return None
        return user[0]
    

    def current_user(self, request: Request) -> TypeVar("User"):
        """Returns a user instance based on cookie value"""
        from models import storage
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        session = storage.search_key_value("Session", "id", session_id)
        if not session:
            return None
        user = storage.search_key_value("User", "id", session[0].user_id)
        if not user:
            return None
        return user[0]
    

    def destroy_session(self, request: Request) -> bool:
        """Deletes a sesssion"""
        from models import storage
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        session = storage.search_key_value("Session", "id", session_id)
        if not session:
            return False
        user = storage.search_key_value("User", "id", session[0].user_id)
        if not user:
            return False
        storage.delete(session[0])
        storage.save()
        return True