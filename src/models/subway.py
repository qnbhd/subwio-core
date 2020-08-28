from sqlalchemy import Column, Integer, String, Float
from src.geopoint import GeoPoint
from .base import Base


class Subway(Base, GeoPoint):
    __tablename__ = 'subways'
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    line_name = Column(String)
    subway_name = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

    def __init__(self, city, line, name, long, lat):
        super().__init__(long, lat)
        self.city_name = city
        self.line_name = line
        self.subway_name = name

    @property
    def point(self):
        return self.longitude, self.latitude

    def __str__(self):
        return f"<'{self.subway_name}'>"

    def __repr__(self):
        return self.__str__()



