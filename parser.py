from bs4 import BeautifulSoup
from datetime import date, datetime
from pathlib import Path
from pydantic import BaseModel
import requests
from requests.exceptions import HTTPError


STATIC_ROOT = './static/'
URL = 'https://rp5.ru/responses/reFileSynop.php'


class WeatherStation(BaseModel):
    ws_id: int = None
    city: str
    link: str
    latitude: float = None
    longitude: float = None
    start_date: date = None


def read_new_cities() -> list:
    stations: list[WeatherStation] = list()
    with open(f"{STATIC_ROOT}cities.txt", 'r', encoding="utf-8") as f:
        for line in f:
            temp = line.strip('\n').split('#')
            if temp[2] == '0':
                stations.append(WeatherStation(city=temp[0], link=temp[1]))
    return stations


def get_missing_ws_info(stations) -> list:
    def get_start_date(s: str) -> date:
        months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                  'ноября', 'декабря', ]
        s = s.removeprefix(' номер метеостанции     , наблюдения с ')
        date_list: list
        date_list = s.strip(' ').split(' ')
        date_list[0] = int(date_list[0])
        date_list[1] = months.index(date_list[1])+1
        date_list[2] = int(date_list[2])
        start_date = date(date_list[2], date_list[1], date_list[0])
        return start_date

    ws: WeatherStation
    for ws in stations:
        try:
            response = requests.get(ws.link)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            ws.ws_id = soup.find("input", id="wmo_id").get('value')
            ws.start_date = get_start_date(soup.find("input", id="wmo_id").parent.text)
    return stations


def create_directory(ws: WeatherStation):
    Path(f"{STATIC_ROOT}{ws.city}").mkdir(parents=True, exist_ok=True)


def get_weather_for_year(year, weather_station):
    if year <= datetime.now().year:
        if datetime.now().date() > date(year, 12, 31):
            last_date = date(year, 12, 31)
        else:
            last_date = datetime.now()
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '108',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'PHPSESSID=3230f98172005d6cec8148fc21a46a56; located=1; extreme_open=false; full_table=1; '
                      'tab_wug=1; ftab=2; tab_metar=1; zoom=11; i=6106%7C3708%7C4012%7C5174%7C6151; '
                      'iru=6106%7C3708%7C4012%7C5174%7C6151; ru=%D0%9D%D0%BE%D1%80%D0%B8%D0%BB%D1%8C%D1%81%D0%BA%7C%D0'
                      '%9A%D0%B0%D0%BB%D1%83%D0%B3%D0%B0%7C%D0%9A%D0%B8%D1%80%D0%BE%D0%B2+%28%D1%80%D0%B0%D0%B9%D0%BE'
                      '%D0%BD%D0%BD%D1%8B%D0%B9+%D1%86%D0%B5%D0%BD%D1%82%D1%80%29%7C%D0%9C%D0%B0%D0%BB%D0%BE%D1%8F%D1'
                      '%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%B5%D1%86%7C%D0%9E%D0%B1%D0%BD%D0%B8%D0%BD%D1%81%D0%BA; '
                      'last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9E%D0%B1'
                      '%D0%BD%D0%B8%D0%BD%D1%81%D0%BA%D0%B5; tab_synop=2; format=xls; f_enc=ansi; lang=ru',
            'Host': 'rp5.ru',
            'Origin': 'https://rp5.ru',
            'Referer': 'https://rp5.ru/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.'
                          '0.4389.90 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        def send_query(h):
            response = requests.post(
                URL,
                data={
                    'wmo_id': weather_station,
                    'a_date1': f'01.01.{year}',
                    'a_date2': last_date.strftime('%d.%m.%Y'),
                    'f_ed3': 3,
                    'f_ed4': 3,
                    'f_ed5': 27,
                    'f_pe': 1,
                    'f_pe1': 2,
                    'lng_id': 2,
                },
                headers=h,
            )
            return response

        response = send_query(headers)
        index: int = 1
        while response.text == 'Error #FS000;':
            print(f"Попытка {index}. {response.text}")
            index += 1
            response = send_query(headers)
        # removeprefix('<script type="text/javascript">$("#f_result").empty().append(\'<a href=')
        print(response.text)
        return datetime.now().date()
    else:
        raise ValueError(f"Запрос погоды из будущего года {year}!")


new_stations = read_new_cities()
if new_stations:
    get_missing_ws_info(new_stations)

station: WeatherStation
for station in new_stations:
    create_directory(station)
    start_year: int = station.start_date.year
    while start_year < datetime.now().year + 1:
        get_weather_for_year(start_year, station.ws_id)
        break
        start_year += 1
    break
