import functools

from typing import List, Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.subway import Base, Subway
from src.models.transition import Transition
from src.subway_graph import SubwayGraph

DB_NAME = 'subwio.db'


def get_city_subways_from_db(session, city_name: str) -> List[Subway]:
    return session.query(Subway).filter_by(city_name=city_name).all()


def get_city_transitions_from_db(session, city_name: str) -> List[Tuple[str, str]]:
    return session.query(Transition).filter_by(city_name=city_name).all()


def create_lines_dict(subways):
    lines_dict = dict()
    for instance in subways:
        if instance.line_name in lines_dict:
            lines_dict[instance.line_name].append(instance)
        else:
            lines_dict[instance.line_name] = []
    return lines_dict


def db_connect(db_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            engine = create_engine(f'sqlite:///{db_name}', echo=False)
            Base.metadata.create_all(engine)
            session = sessionmaker(bind=engine)()
            result = func(session, *args, **kwargs)
            return result

        return wrapper

    return decorator


@db_connect(DB_NAME)
def main(session):
    CURRENT_CITY = ''
    subways = get_city_subways_from_db(session, CURRENT_CITY)
    transitions = get_city_transitions_from_db(session, CURRENT_CITY)
    lines_dict = create_lines_dict(subways)

    graph = SubwayGraph(CURRENT_CITY, lines_dict, transitions)


if __name__ == '__main__':
    main()
