#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """ State class 
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan', backref="state")

    @property
    def cities(self):
        all_obj = models.storage.all()
        my_list = []
        res = []
        for key in all_obj:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                my_list.append(all_obj[key])
        for element in my_list:
            if (element.state_id == self.id):
                res.append(element)
        return(res)
