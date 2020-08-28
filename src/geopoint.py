class GeoPoint:

    def __init__(self, longitude, latitude):
        self.latitude = latitude
        assert 0 <= latitude <= 90, 'latitude must be in [0; 90] degrees'
        self.longitude = longitude
        assert 0 <= longitude <= 180, 'longitude must be in [0; 180] degrees'

    def __str__(self):
        return f'<lat: {self.latitude} long: {self.longitude}>'
