#!/usr/bin/python3
"""Module containing error handling classes"""
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


class Unauthorized(HTTPException):
    """Handles Unauthorized access"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_401_UNAUTHORIZED,
                         detail=detail if detail else "Unauthorized")