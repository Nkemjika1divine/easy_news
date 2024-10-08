#!/usr/bin/python3
"""Module containing error handling classes"""
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


class Unauthorized(HTTPException):
    """Handles Unauthorized access"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_401_UNAUTHORIZED,
                         detail=detail if detail else "Unauthorized")


class Forbidden(HTTPException):
    """Handles Forbidden access"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_403_FORBIDDEN,
                         detail=detail if detail else "Forbidden")


class Not_Found(HTTPException):
    """Handles Not found error"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND,
                         detail=detail if detail else "Not Found")


class Bad_Request(HTTPException):
    """Handles Bad requests or incomplete request"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_400_BAD_REQUEST,
                         detail=detail if detail else "Incomplete Request")


class Server_Error(HTTPException):
    """Handles Bad requests or incomplete request"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                         detail=detail if detail else "Internal Server Error")