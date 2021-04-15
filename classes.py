from pydantic import BaseModel
from datetime import date


class WeatherStation(BaseModel):
    link: str
    ws_id: int = None
    country: str = None
    city_id: int = None
    city: str = None
    latitude: float = None
    longitude: float = None
    start_date: date = None

    # '%Y, %-m, %d' if you are using Unix system
    def __str__(self):
        return f"WeatherStation(ws_id={self.ws_id}, country=\"{self.country}\", city=\"{self.city}\", " \
               f"city_id={self.city_id}, latitude={self.latitude}, longitude={self.longitude}, " \
               f"start_date=date({self.start_date.strftime('%Y, %#m, %d')}))"

    def __repr__(self):
        return f"WeatherStation(ws_id={self.ws_id}, country=\"{self.country}\", city=\"{self.city}\", " \
               f"city_id={self.city_id}, latitude={self.latitude}, longitude={self.longitude}, " \
               f"start_date=date({self.start_date.strftime('%Y, %#m, %d')}))"

    def to_csv(self, delimiter):
        return f"{self.city}{delimiter}{self.link}{delimiter}" \
               f"{'None' if self.start_date is None else self.start_date.strftime('%Y-%m-%d')}" \
               f"{delimiter}{self.ws_id}{delimiter}{self.country}{delimiter}{self.city_id}{delimiter}" \
               f"{self.latitude}{delimiter}{self.longitude}"
