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
    if not email or type(email) is not str or len(email) > 50:
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


@user_router.put("/users/change_email")
async def change_email(request: Request) -> str:
    from models import storage
    """PUT method that changes a user's email"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    email = request_body.get("email", None)
    if not email or type(email) is not str or len(email) > 50:
        raise Bad_Request("Email missing or not a string")
    if not validate_email_pattern(email):
        raise Forbidden("Wrong email format")
    existing_user = storage.search_key_value("User", "email", email)
    if existing_user:
        raise Forbidden("Email already registered")
    user = request.state.current_user
    user.email = email
    user.email_verified = "no"
    user.email_token = generate_token()
    storage.save()
    user.send_email_token()
    return JSONResponse(content="Email successfully updated", status_code=status.HTTP_200_OK)


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


@user_router.get("/users/get_password_reset_token")
def get_password_reset_token(request: Request) -> str:
    """GET method that sends password reset token to the user's email"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    user = request.state.current_user
    token = user.generate_password_token(user.id)
    if token:
        if user.send_password_token():
            return JSONResponse(content=("Token successfully sent"), status_code=status.HTTP_200_OK)
        raise Server_Error("Failed to send password token")
    raise Server_Error("Failed to generate token")


@user_router.put("/users/change_password")
async def change_password(request: Request) -> str:
    """PUT method that changes a user's password"""
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
    if len(password) > 20 or len(password) < 8:
        raise Bad_Request("Password length must be between 8 to 20 characters")
    user = request.state.current_user
    user.update_password(password)
    return JSONResponse(content="Password successfully updated", status_code=status.HTTP_200_OK)


@user_router.get("/users/profile")
def get_user_profile(request: Request) -> str:
    """GET method that returns the user's profile"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    user = request.state.current_user
    user_dict = user.to_safe_json()
    # Get the channels the user is following and add it to the dictionary
    user_channels = storage.search_key_value("User_Channel", "user_id", user.id)
    if user_channels:
        channels_user_follows = []
        for user_channel in user_channels:
            channels_user_follows.append(user_channel.name)
        user_dict['channels_user_follows'] = channels_user_follows
    else:
        user_dict['channels_user_follows'] = None
    # Get the categories the user is following and add it to the dictionary
    user_dict = user.to_safe_json()
    user_categories = storage.search_key_value("User_Category", "user_id", user.id)
    if user_categories:
        categories_user_follows = []
        for user_category in user_categories:
            categories_user_follows.append(user_category.category_name)
        user_dict['categories_user_follows'] = categories_user_follows
        return JSONResponse(content=user_dict, status_code=status.HTTP_200_OK)
    else:
        user_dict['categories_user_follows'] = None
    return JSONResponse(content=user_dict, status_code=status.HTTP_200_OK)


@user_router.put("/users/change_name")
async def change_name(request: Request) -> str:
    """PUT method that changes a user's name"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    name = request_body.get("name", None)
    if not name or type(name) is not str or len(name) > 50:
        raise Bad_Request("Name missing or not a string or more than 50 characters")
    user = request.state.current_user
    user.name = name
    storage.save()
    return JSONResponse(content="Name updated successfully", status_code=status.HTTP_200_OK)


@user_router.put("/users/promote/{user_id}")
def upgrade_user_role(request: Request, user_id: str = None) -> str:
    """PUT method for upgrading a user to admin"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not user_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    current_user = request.state.current_user
    if current_user.role == "user" or current_user.role == "admin":
        raise Unauthorized("You are not authorized to perform this operation")
    user = storage.search_key_value("User", "id", user_id)
    if not user:
        raise Not_Found("User does not exist")
    if user[0].role == 'admin':
        raise Unauthorized("User already an admin")
    user[0].role = "admin"
    storage.save()
    return JSONResponse(content="{} promoted to admin successfully".format(user[0].name), status_code=status.HTTP_200_OK)


@user_router.put("/users/demote/{user_id}")
def upgrade_user_role(request: Request, user_id: str = None) -> str:
    """PUT method for demoting a user from admin"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not user_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    current_user = request.state.current_user
    if current_user.role == "user" or current_user.role == "admin":
        raise Unauthorized("You are not authorized to perform this operation")
    user = storage.search_key_value("User", "id", user_id)
    if not user:
        raise Not_Found("User does not exist")
    if user[0].role == 'user':
        raise Unauthorized("User already a simple user")
    user[0].role = "user"
    storage.save()
    return JSONResponse(content="{} demoted to user successfully".format(user[0].name), status_code=status.HTTP_200_OK)


@user_router.delete("/users/delete_my_account")
def delete_my_account(request: Request) -> str:
    """DELETE method that deletes a user's account by the user"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    user = request.state.current_user
    storage.delete(user)
    storage.save()
    return JSONResponse(content="User succesfully deleted", status_code=status.HTTP_200_OK)


@user_router.delete("/users/{user_id}")
def delete_my_account(request: Request, user_id: str = None) -> str:
    """DELETE method that deletes a user's account by the user"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not user_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    current_user = request.state.current_user
    if current_user.role == "user":
        raise Unauthorized("You are not authorized to perform this task")
    user = storage.search_key_value("User", "id", user_id)
    if not user:
        raise Not_Found("User does not exist")
    storage.delete(user[0])
    storage.save()
    return JSONResponse(content="User succesfully deleted", status_code=status.HTTP_200_OK)
