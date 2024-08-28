#!/usr/bin/python3
"""Module deploying our Easy News FastAPI app"""
from api.v1.endpoints.users import user_router
from api.v1.error_handlers import Unauthorized, Forbidden
from auth.auth import Auth
from auth.middleware.middleware import AuthMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


load_dotenv()


app = FastAPI()
api_prefix = "/api/v1"
app.include_router(user_router, prefix=api_prefix)


path_list = [
             '/docs',
             '/api/v1/users/register',
             '/api/v1/categories'
             ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # URLs to allow
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE all allowed
    allow_headers=["*"]  # All headers allowed
)


@app.exception_handler(Unauthorized)
async def unauthorized_handler(request: Request, exc: Unauthorized):
    """Handles Unauthorized exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.exception_handler(Forbidden)
async def forbidden_handler(request: Request, exc: Forbidden):
    """Handles Forbidden exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


auth = Auth()
app.add_middleware(AuthMiddleware, auth=auth, excluded_paths=path_list)