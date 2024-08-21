#!/usr/bin/python3
"""The Database Module"""
from dotenv import load_dotenv
from models.basemodel import Base
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict, TypeVar, List


load_dotenv()


classes = {} # will contain all models


class DB:
    """The Database Class
    - Handles all database operations
    """
    __session = None
    __engine = None

    def __init__(self) -> None:
        """Initializing the Database"""
        EN_DB = environ.get("EN_DB")
        EN_PORT = environ.get("EN_PORT")
        EN_USER = environ.get("EN_USER")
        EN_PWD = environ.get("EN_PWD")
        EN_HOST = environ.get("EN_HOST")

        if not all([EN_DB, EN_PORT, EN_USER, EN_PWD, EN_HOST]):
            raise ValueError("One or more environment variables are missing")
        
        self.__engine = create_engine(
            "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(EN_USER,
                                                           EN_PWD,
                                                           EN_HOST,
                                                           EN_PORT,
                                                           EN_DB))
        if environ.get("EN_ENV") == "test":
            try:
                Base.metadata.drop_all(self.__engine)
            except Exception:
                print("There is no table in the database")