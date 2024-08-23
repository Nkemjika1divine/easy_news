#!/usr/bin/python3
"""Module containing /users* endpoints"""
from api.v1.error_handlers import *
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.user import User
from os import environ
from utils.utility import validate_email_pattern


user_router = APIRouter()


@user_router.post("/users/register")
async def register_user(request: Request) -> str:
    """POST request to register a user"""
    from auth.auth import Auth
    from models import storage
    if not request:
        raise Bad_Request()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    if not storage.all("User"):
        role = 'superuser'
    else:
        role = 'user'
    name = request_body.get("name", None)
    if not name or type(name) is not str or len(name) > 50:
        raise Bad_Request("name must be a string and must not exceed 50 characters")
    email = request_body.get("email", None)
    if not email or type(email) is not str or len(name) > 50:
        raise Bad_Request("Email missing or not a string")
    if not validate_email_pattern(email):
        raise Forbidden("Wrong email format")
    existing_user = storage.search_key_value("User", "email", email)
    if existing_user:
        raise Forbidden("Email already registered")
    password = request_body.get("password", None)
    if not password or type(password) is not str:
        raise Bad_Request("Password missing or not a string")
    if len(password) > 20 or len(password) < 8:
        raise Bad_Request("Password length must be greater than 7 and less than 21")
    
    user = User(name=name, email=email, password=password, role=role)
    user.save()
    auth = Auth()
    session_id = auth.create_session(user.id)
    expiry_date = datetime.now(timezone.utc) + timedelta(days=30)
    response = JSONResponse(content=user.to_safe_dict(), status_code=status.HTTP_201_CREATED)
    response.set_cookie(key=environ.get("SESSION_NAME"), value=session_id, expires=expiry_date)
    return response



