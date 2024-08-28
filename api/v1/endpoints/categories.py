#!/usr/bin/python3
"""Module containing /categories* endpoints"""
from api.v1.error_handlers import *
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.category import Category


categories_router = APIRouter()


@categories_router.post("/categories/add")
async def add_a_category(request: Request) -> str:
    """POST method that adds a new category"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    category_name = request_body.get("name", None)
    if not category_name or type(category_name) is not str or len(category_name) > 50:
        raise Bad_Request("category name must be a string and must not exceed 50 characters")
    category = Category()
    category.category_name = category_name.lower()
    category.save()
    return JSONResponse(content=f"{category_name} saved successfully")