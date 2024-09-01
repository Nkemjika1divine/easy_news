#!/usr/bin/python3
"""Module containing /users/channels* endpoints"""
from api.v1.error_handlers import *
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.user_channel import User_Channel


user_channel_router = APIRouter()


@user_channel_router.post("/users/channels/add")
async def add_channel_to_user(request: Request) -> str:
    """POST method that allows a user to choose a channel to follow"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    channel_name = request_body.get("channel_name", None)
    if not channel_name or type(channel_name) is not str or len(channel_name) > 50:
        raise Bad_Request("chanel_name must be a string and must not exceed 50 characters")
    channel = storage.search_key_value("Channel", "channel_name", channel_name)
    if not channel:
        raise Not_Found(f"{channel_name} does not exist")
    user_channel = User_Channel()
    user_channel.channel_id = channel[0].id
    user_channel.user_id = request.state.current_user.id
    user_channel.save()
    return JSONResponse(content="User following the channel successfully", status_code=status.HTTP_200_OK)