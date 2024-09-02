#!/usr/bin/python3
"""Module containing /users/categories* endpoints"""
from api.v1.error_handlers import *
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.user_category import User_Category


user_category_router = APIRouter()


@user_category_router.post("/users/categories/add")
async def add_new_category(request: Request) -> str:
    """POST method that allows a user to follow a category"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    category_name = request_body.get("category_name", None)
    if not category_name or type(category_name) is not str or len(category_name) > 50:
        raise Bad_Request("category_name must be a string and must not exceed 50 characters")
    category = storage.search_key_value("Category", "category_name", category_name)
    if not category:
        raise Not_Found(f"{category_name} does not exist")
    user_category = User_Category()
    user_category.category_id = category[0].id
    user_category.user_id = request.state.current_user.id
    user_category.save()
    return JSONResponse(content="User following the category successfully", status_code=status.HTTP_200_OK)


