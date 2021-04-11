from bs4 import BeautifulSoup
from datetime import date, datetime
import zlib
from pathlib import Path
from pydantic import BaseModel
from requests.exceptions import HTTPError
from requests import Session


STATIC_ROOT = './static/'
URL = 'https://rp5.ru/responses/reFileSynop.php'
current_session: Session = Session()
DELIMITER = '#'


class WeatherStation(BaseModel):
    ws_id: int = None
    city: str
    link: str
    latitude: float = None
    longitude: float = None
    start_date: date = None

    def to_csv(self, delimiter):
        if self.start_date is None:
            return f"{self.city}{delimiter}{self.link}"
        return f"{self.city}{delimiter}{self.link}{delimiter}" \
               f"{self.start_date.strftime('%Y-%m-%d')}{delimiter}{self.ws_id}"


def read_new_cities(delimiter: str) -> [WeatherStation]:
    """Get data about new weather stations from csv file for site rp5.ru.
    Csv file structure:
    -city;
    -link on weathers archive page for city in site rp5.ru;
    -nothing or last date of loaded information;
    -nothing or id of weather station."""

    stations: list[WeatherStation] = list()
    with open(f"{STATIC_ROOT}cities.txt", 'r', encoding="utf-8") as f:
        for line in f:
            temp = line.strip('\n').split(delimiter)
            if len(temp) > 2:
                stations.append(WeatherStation(
                    city=temp[0],
                    link=temp[1],
                    start_date=datetime.strptime(temp[2], '%Y-%m-%d').date(),
                    ws_id=int(temp[3])))
            else:
                stations.append(WeatherStation(city=temp[0], link=temp[1]))
    return stations


def get_missing_ws_info(station: WeatherStation) -> WeatherStation:
    """Getting start date of observations and numbers weather station from site rp5.ru."""

    global current_session

    def get_start_date(s: str) -> date:
        """Function get start date of observations for current weather station."""

        months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
                  'августа', 'сентября', 'октября', 'ноября', 'декабря', ]
        s = s.removeprefix(' номер метеостанции     , наблюдения с ')
        date_list: list = s.strip(' ').split(' ')
        year = int(date_list[2])
        month = months.index(date_list[1]) + 1
        day = int(date_list[0])
        start_date: date = date(year, month, day)
        return start_date

    try:
        response = current_session.get(station.link)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        station.ws_id = soup.find("input", id="wmo_id").get('value')
        station.start_date = get_start_date(soup.find("input", id="wmo_id").parent.text)
    return station


def create_directory(ws: WeatherStation):
    Path(f"{STATIC_ROOT}{ws.city}").mkdir(parents=True, exist_ok=True)


def get_text_with_link_on_weather_data_file(ws_id: int, start_date: date, last_date: date):
    """Function create query for site rp5.ru with special params for
    getting JS text with link on csv.gz file and returns response of query.
    I use session and headers because site return text - 'Error #FS000;'
    in otherwise."""

    global current_session
    current_session.headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '108',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'PHPSESSID={current_session.cookies.items()[0][1]}; located=1; extreme_open=false; full_'
                  f'table=1; tab_wug=1; ftab=2; tab_metar=1; zoom=11; i=6106%7C3708%7C4012%7C5174%7C6151; '
                  f'iru=6106%7C3708%7C4012%7C5174%7C6151; ru=%D0%9D%D0%BE%D1%80%D0%B8%D0%BB%D1%8C%D1%81%D0%BA'
                  f'%7C%D0%9A%D0%B0%D0%BB%D1%83%D0%B3%D0%B0%7C%D0%9A%D0%B8%D1%80%D0%BE%D0%B2+%28%D1%80%D0%B0%D0'
                  f'%B9%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9+%D1%86%D0%B5%D0%BD%D1%82%D1%80%29%7C%D0%9C%D0%B0%D0%BB%D0'
                  f'%BE%D1%8F%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%B5%D1%86%7C%D0%9E%D0%B1%D0%BD%D0%B8%D0%BD'
                  f'%D1%81%D0%BA; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_'
                  f'%D0%B2_%D0%9E%D0%B1%D0%BD%D0%B8%D0%BD%D1%81%D0%BA%D0%B5; tab_synop=2; format=xls; '
                  f'f_enc=ansi; lang=ru',
        'Host': 'rp5.ru',
        'Origin': 'https://rp5.ru',
        'Referer': 'https://rp5.ru/',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        result = current_session.post(
            URL,
            data={'wmo_id': ws_id, 'a_date1': start_date.strftime('%d.%m.%Y'),
                  'a_date2': last_date.strftime('%d.%m.%Y'), 'f_ed3': 3, 'f_ed4': 3, 'f_ed5': 27, 'f_pe': 1,
                  'f_pe1': 2, 'lng_id': 2, })
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return result


def get_link_archive_file(text: str) -> str:
    """Function extract link on archive file with weather data from text."""

    start_position: int = text.find('<a href=http')
    end_position: int = text.find('.csv.gz')
    if start_position > -1 and end_position > -1:
        link: str = text[start_position + 8:end_position + 7]
    else:
        raise ValueError(f'Ссылка на скачивание архива не найдена! Text: "{text}"')
    return link


def get_weather_for_year(start_date: date, ws_id: int, city: str):
    """Function get archive file from site rp5.ru with weather data for one year
    and save it at directory."""

    global current_session
    if start_date.year <= datetime.now().year:
        if datetime.now().date() > date(start_date.year, 12, 31):
            last_date: date = date(start_date.year, 12, 31)
        else:
            last_date: date = datetime.now().date()

        answer = get_text_with_link_on_weather_data_file(ws_id, start_date, last_date)

        download_link = get_link_archive_file(answer.text)

        with open(f'{STATIC_ROOT}{city}/{start_date.year}.csv', "wb") as file:
            response = current_session.get(download_link)
            while response.status_code != 200:
                response = current_session.get(download_link)

            decompress = zlib.decompress(response.content, wbits=zlib.MAX_WBITS | 16)
            csv_weather_data: list = decompress.decode('utf-8').splitlines()
            del csv_weather_data[:7]
            # print(csv_weather_data)
            # file.write(decompress)
        return None
    else:
        raise ValueError(f"Запрос погоды из будущего {start_date.year} года!")


def update_csv_file(wanted_stations: [WeatherStation], delimiter):
    """Function update file with our wanted weather stations.
    It write current date and id of weather station."""

    with open(f"{STATIC_ROOT}cities.txt", "w", encoding="utf-8") as csv_file:
        csv_data = ""
        for station in wanted_stations:
            csv_data = f"{csv_data}{station.to_csv(delimiter)}\n"
        csv_file.write(csv_data)


def get_all_data_for_weather_stations():
    """Function get all weather data for new weather stations from csv file
    from start date of observations to today."""

    wanted_stations = read_new_cities(DELIMITER)

    if wanted_stations:

        station: WeatherStation
        for station in wanted_stations:
            if station.start_date is None or station.ws_id is not None:
                get_missing_ws_info(station)
            create_directory(station)
            start_year: int = station.start_date.year
            while start_year < datetime.now().year + 1:
                if start_year == station.start_date.year:
                    start_date: date = station.start_date
                else:
                    start_date: date = date(start_year, 1, 1)
                get_weather_for_year(start_date, station.ws_id, station.city)
                start_year += 1
                # Now is tested but then must be deleted
                break
            break

    update_csv_file(wanted_stations, DELIMITER)
    return


def get_data_for_weather_stations_with_end_date():
    """Function get weather data for weather stations from csv file
    from ended date of last downloads to today."""

    pass


get_all_data_for_weather_stations()
