from sqlalchemy import Column, Integer, String, Date, Float
from .base import Base


class Transition(Base):
    __tablename__ = 'transitions'
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    subway1 = Column(String)
    subway2 = Column(String)

    def __init__(self, city, sub1, sub2):
        self.city_name = city
        self.subway1 = sub1
        self.subway2 = sub2

    def __repr__(self):
        return f"<'{self.city_name} between {self.subway1}, {self.subway2}"
