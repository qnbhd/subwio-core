from geopy import distance


class Metric:
    @staticmethod
    def metric(point1, point2):
        return distance.distance(point1, point2).km
