#!/usr/bin/python3
""" Place Module for HBNB project """

from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models

place_amenity = Table("place_amenity", Base.metadata, Column(
    "place_id", String(60), ForeignKey(
        "places.id"), primary_key=True, nullable=False), Column(
            "amenity_id", String(60), ForeignKey(
                "amenities.id"), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
                "Review", cascade='all, delete, delete-orphan',
                backref="place")
        amenities = relationship(
                "Amenity", secondary=place_amenity, viewonly=False,
                back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """method that returns list of reviews.id"""
            all_obj = models.storage.all()
            my_list = []
            res = []
            for key in my_list:
                review = key.replace('.', ' ')
                review = shlex.split(review)
                if (review[0] == "Review"):
                    my_list.append(all_obj[key])
            for element in my_list:
                if (element.place_id == self.id):
                    res.append(element)
            return (res)

        @property
        def amenities(self, obj=None):
            """Method that returns list of amenity ids"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """method that append amenities ids to the attribute"""
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
