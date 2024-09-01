#!/usr/bin/python3
"""Module containing /categories* endpoints"""
from api.v1.error_handlers import *
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.category import Category


category_router = APIRouter()


@category_router.post("/categories/add")
async def add_a_category(request: Request) -> str:
    """POST method that adds a new category"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.role == 'user':
        raise Unauthorized("You are not authorized to perform this operation")
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    category_name = request_body.get("category_name", None)
    if not category_name or type(category_name) is not str or len(category_name) > 50:
        raise Bad_Request("category name must be a string and must not exceed 50 characters")
    category = Category()
    category.category_name = category_name.lower()
    category.save()
    return JSONResponse(content=f"{category_name} saved successfully", status_code=status.HTTP_200_OK)


@category_router.put("/categories/{category_id}")
async def add_a_category(request: Request, category_id: str = None) -> str:
    """POST method that adds a new category"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not category_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.role == 'user':
        raise Unauthorized("You are not authorized to perform this operation")
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    category = storage.search_key_value("Category", "id", category_id)
    if not category:
        raise Not_Found("Category does not exist")
    category_name = request_body.get("category_name", None)
    if not category_name or type(category_name) is not str or len(category_name) > 50:
        raise Bad_Request("category name must be a string and must not exceed 50 characters")
    category[0].category_name = category_name.lower()
    storage.save()
    return JSONResponse(content=f"{category_name} updated successfully", status_code=status.HTTP_200_OK)


@category_router.get("/categories")
def get_all_categories(request: Request) -> str:
    """GET method that returns all categories"""
    from models import storage
    if not request:
        raise Bad_Request()
    all_categories = storage.all("Category")
    if not all_categories:
        raise Not_Found("No categories found")
    category_list = []
    for category in all_categories.values():
        category_list.append(category.to_dict())
    return JSONResponse(content=category_list, status_code=status.HTTP_200_OK)


@category_router.delete("/categories/{category_id}")
def delete_a_category(request: Request, category_id: str = None) -> str:
    """POST method that adds a new category"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not category_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.role == 'user':
        raise Unauthorized("You are not authorized to perform this operation")
    category = storage.search_key_value("Category", "id", category_id)
    if not category:
        raise Not_Found("Category does not exist")
    storage.delete(category[0])
    storage.save()
    return JSONResponse(content="Category successfully deleted", status_code=status.HTTP_200_OK)