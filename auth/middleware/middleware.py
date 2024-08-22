#!/usr/bin/python3
""" Module Handles middleware operations"""
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware"""

    def __init__(self, app, auth, excluded_paths: List[str]):
        """'Handles Initialization of the middleware'"""
        super().__init__(app)
        self.auth = auth
        self.excluded_paths = excluded_paths