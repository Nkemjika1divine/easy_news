#!/usr/bin/python3
"""Module containing /channels* endpoints"""
from api.v1.error_handlers import *
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from models.channel import Channel


channel_router = APIRouter()


@channel_router.post("/channels/add")
async def add_new_channel(request: Request) -> str:
    """POST method that adds a new channel"""
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
    channel_name = request_body.get("channel_name", None)
    if not channel_name or type(channel_name) is not str or len(channel_name) > 50:
        raise Bad_Request("chanel_name must be a string and must not exceed 50 characters")
    source = request_body.get("source", None)
    if not source or type(source) is not str or len(source) > 50:
        raise Bad_Request("source must be a string and must not exceed 50 characters")
    channel = Channel(channel_name=channel_name, source=source)
    channel.save()
    return JSONResponse(content=channel.to_dict(), status_code=status.HTTP_200_OK)


@channel_router.put("/channels/edit/{channel_id}")
async def edit_channel(request: Request, channel_id: str = None) -> str:
    """PUT method that edits a channel"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not channel_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.role == 'user':
        raise Unauthorized("You are not authorized to perform this operation")
    channel = storage.search_key_value("Channel", "id", channel_id)
    if not channel:
        raise Not_Found("Channel not found in the database")
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    if 'channel_name' in request_body:
        channel_name = request_body['channel_name']
        if type(channel_name) is not str or len(channel_name) > 50:
            raise Bad_Request("chanel_name must be a string and must not exceed 50 characters")
        channel[0].channel_name = channel_name
    if 'source' in request_body:
        source = request_body['source']
        if type(source) is not str or len(source) > 50:
            raise Bad_Request("source must be a string and must not exceed 50 characters")
        channel[0].source = source
    storage.save()
    return JSONResponse(content="Channel updated successfully", status_code=status.HTTP_200_OK)


@channel_router.get("/channels")
def get_all_channels(request: Request) -> str:
    """GET method that returns all channels"""
    from models import storage
    if not request:
        raise Bad_Request()
    channels = storage.all("Channel")
    if not channels:
        raise Not_Found("No channels found in the database")
    channel_list = []
    for channel in channels.values():
        channel_list.append(channel.to_dict())
    return JSONResponse(content=channel_list, status_code=status.HTTP_200_OK)