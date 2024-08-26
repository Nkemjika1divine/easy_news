#!/usr/bin/python3
"""Module containing /users* endpoints"""
from api.v1.error_handlers import *
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.user import User
from os import environ
from utils.utility import validate_email_pattern, generate_token


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
        raise Bad_Request("Password length must be between 8 to 20 characters")
    # Create the user
    user = User(name=name, email=email, password=password, role=role, email_token=generate_token())
    user.save()
    user.send_email_token()
    auth = Auth()
    session_id = auth.create_session(user.id)
    expiry_date = datetime.now(timezone.utc) + timedelta(days=30)
    response = JSONResponse(content=user.to_safe_dict(), status_code=status.HTTP_200_OK)
    response.set_cookie(key=environ.get("SESSION_NAME"), value=session_id, expires=expiry_date)
    return response


@user_router.post("/users/verify_email")
async def verify_email(request: Request) -> str:
    """POST method for email verification"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    code = request_body.get("code", None)
    if not code or type(code) is not str:
        raise Bad_Request("code missing or not a string")
    user = request.state.current_user
    if code != user.email_token:
        raise Unauthorized("Wrong code entered")
    user.email_verified = "yes"
    user.email_token = None
    storage.save()
    return JSONResponse(content="Email successfully verified", status_code=status.HTTP_200_OK)


@user_router.post("/users/confirm_password")
async def confirm_password(request: Request) -> str:
    """POST method that confirms a user's password"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    password = request_body.get("password", None)
    if not password or type(password) is not str:
        raise Bad_Request("Password missing or not a string")
    user = request.state.current_user
    if user.is_valid_password(password):
        return JSONResponse(content="Password accepted", status_code=status.HTTP_200_OK)
    raise Unauthorized("Password do not match")


@user_router.put("/users/send_email_verification_code")

