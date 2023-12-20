#!/usr/bin/python3
"""new engine for ORM - SQLAlchemy"""

from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """class that create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                    user, passwd, host, db), pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """method that return a dictionary.
        Args:
            cls (str): None
        Return:
            __object
        """
        my_dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                my_dic[key] = elem
        else:
            my_list = [State, City, User, Place, Review, Amenity]
            for clas in my_list:
                query = self.__session.query(clas)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__.elem.id)
                    my_dic[key] = elem
        return(my_dic)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database
        and create the current database session
        """
        Base.metadata.create_all(self.__engine)
        sc = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sc)
        self.__session = Session()

    def close(self):
        """method that calls remove()"""
        self.__session.close()
