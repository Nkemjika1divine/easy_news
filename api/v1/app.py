#!/usr/bin/python3
"""Module deploying our Easy News FastAPI app"""
from auth.auth import Auth
from auth.middleware.middleware import AuthMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()


app = FastAPI()


path_list = [
             '/docs',
             ]


auth = Auth()
app.add_middleware(AuthMiddleware, auth=auth, excluded_paths=path_list)