from pydantic import BaseModel
from datetime import date


class WeatherStation(BaseModel):
    city: str = None
    link: str
    # 0 - weather station, 1 - metar, 2 - weather sensor
    data_type: int
    number: int = None
    country: str = None
    ws_id: int = None
    latitude: float = None
    longitude: float = None
    start_date: date = None

    # '%Y, %-m, %d' if you are using Unix system
    def __str__(self):
        return f"WeatherStation(city=\"{self.city}\", link=\"{self.link}\", data_type={self.data_type}," \
               f"number={self.number}, country=\"{self.country}\", ws_id={self.ws_id}, latitude={self.latitude}, " \
               f"longitude={self.longitude}, start_date=date({self.start_date.strftime('%Y, %#m, %d')}))"

    def __repr__(self):
        return f"WeatherStation(city=\"{self.city}\", link=\"{self.link}\", data_type={self.data_type}," \
               f"number={self.number}, country=\"{self.country}\", ws_id={self.ws_id}, latitude={self.latitude}, " \
               f"longitude={self.longitude}, start_date=date({self.start_date.strftime('%Y, %#m, %d')}))"

    def to_csv(self, delimiter):
        return f"{self.city}{delimiter}{self.link}{delimiter}{self.data_type}{delimiter}" \
               f"{'None' if self.start_date is None else self.start_date.strftime('%Y-%m-%d')}" \
               f"{delimiter}{self.number}{delimiter}{self.country}{delimiter}{self.ws_id}{delimiter}" \
               f"{self.latitude}{delimiter}{self.longitude}"
