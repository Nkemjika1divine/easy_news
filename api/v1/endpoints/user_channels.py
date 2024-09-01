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


@user_channel_router.delete("/users/channels/remove/{channel_name}")
def remove_a_follow(request: Request, channel_name: str = None) -> str:
    """DELETE method that stops a user from following a channel"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not channel_name:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    channel = storage.search_key_value("Channel", "channel_name", channel_name)
    if not channel:
        raise Not_Found(f"{channel_name} does not exist")
    user_channels = storage.search_key_value("User_Channel", "channel_id", channel[0].id)
    if not user_channels:
        raise Not_Found(f"{channel_name} has no followers")
    for user_channel in user_channels:
        if user_channel.user_id == request.state.current_user.id:
            storage.delete(user_channel)
            storage.save()
            return JSONResponse(content="Channel successfully unfollowed")
    raise Unauthorized("You are not following this channel")