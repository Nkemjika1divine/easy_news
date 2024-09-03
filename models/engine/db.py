#!/usr/bin/python3
"""The Database Module"""
from dotenv import load_dotenv
from models.basemodel import Base
from models.category import Category
from models.channel import Channel
from models.news import News
from models.notification import Notification
from models.session import Session
from models.user import User
from models.user_category import User_Category
from models.user_channel import User_Channel
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict, TypeVar, List


load_dotenv()


classes = {
    "Category": Category,
    "Channel": Channel,
    "News": News,
    "Notification": Notification,
    "Session": Session,
    "User": User,
    "User_Category": User_Category,
    "User_Channel": User_Channel
} # will contain all models


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
    

    def all(self, cls=None) -> Dict[str, any]:
        """query on the current database session"""
        result = {}
        if cls is not None:
            for obj in self.__session.query(classes[cls]).all():
                ClassName = obj.__class__.__name__
                keyName = ClassName + "." + obj.id
                result[keyName] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls).all():
                    class_name = obj.__class__.__name__
                    key = class_name + "." + obj.id
                    result[key] = obj
        return result
    

    def save(self) -> None:
        """commit all changes of the database"""
        self.__session.commit()
    

    def delete(self, obj=None) -> None:
        """delete an object from the database"""
        if obj:
            self.__session.delete(obj)
    

    def reload(self) -> None:
        """reloads from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
    

    def search_key_value(self, classname: str = None, key: str = None, value: str = None) -> List[TypeVar('BaseModel')]:
        """Search the database for a value based on the key (also column name)"""
        from models import storage
        if not key or not value:
            return []
        if type(key) is not str or type(value) is not str:
            return []
        list_of_objs = []
        all_data = storage.all(classname)
        for obj_value in all_data.values():
            value_dict = obj_value.to_dict()
            if key in value_dict:
                if value_dict[key] == value:
                    list_of_objs.append(obj_value)
        return list_of_objs
    

    def new(self, obj) -> None:
        """add an object to the database"""
        if obj.__class__.__name__ == "User":
            hashed = obj.hash_password(obj.password)
            if not hashed:
                raise ValueError()
            setattr(obj, "password", hashed)
        self.__session.add(obj)