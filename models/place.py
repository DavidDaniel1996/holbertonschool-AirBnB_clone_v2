#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    reviews = relationship("Review", backref='place',
                           cascade='all, delete, delete-orphan')
    amenities = relationship("Amenity", secondary='place_amenity',
                             viewonly=False)
    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews_att(self):
            """Defines review attribute for FileStorage"""
            from models import storage
            reviews_dict = storage.all('Review')
            reviews_list = []
            for key, value in reviews_dict.items():
                if value.place_id == self.id:
                    reviews_list.append(value)
            return reviews_list

        @property
        def amenities(self):
            from models import storage
            amenities_dict = storage.all('Amenity')
            amenities_list = []
            for key, value in amenities_dict.items():
                if value.amenity_id == self.id:
                    amenities_list.append(value)
            return amenities_list

        @amenities.setter
        def amenities_att(self, obj):
            if type(obj).__name__ != 'Amenity':
                return
            self.amenity_ids.append(obj['id'])
