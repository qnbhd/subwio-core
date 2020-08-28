from boltons.setutils import IndexedSet
from src.models.subway import Subway
from sqlalchemy import Column, Integer, String, Date, Float
from .base import Base


class SubwayLine(Base):
    __tablename__ = 'subway_lines'
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    line_name = Column(String)
    color = Column(String)

    def __init__(self, city_name, line_name, folium_color):
        super().__init__()
        self.city_name = city_name
        self.line_name = line_name
        self.color = folium_color

