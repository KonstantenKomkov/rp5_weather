from bs4 import BeautifulSoup
from datetime import date
from requests.exceptions import HTTPError
from requests.models import Response

import rp5_headers
import classes
from requests import Session
import queries


URL = 'https://rp5.ru/responses/reFileSynop.php'


def get_start_date(s: str) -> date:
    """ Function get start date of observations for current weather station."""

    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
              'августа', 'сентября', 'октября', 'ноября', 'декабря', ]
    s = s.removeprefix(' номер метеостанции     , наблюдения с ')
    date_list: list = s.strip(' ').split(' ')
    year = int(date_list[2])
    month = months.index(date_list[1]) + 1
    day = int(date_list[0])
    return date(year, month, day)


def get_coordinates(a: str) -> tuple[float, float]:
    """ Function find latitude and longitude in html string for weather station."""
    if isinstance(a, str):
        if a.find("show_map(") > -1 and a.find(");") > -1 and a.find(", ") > -1:
            temp = a[a.find("show_map(") + 9:a.find(");")].split(", ")
            return float(temp[0]), float(temp[1])
        return None, None
    else:
        raise (TypeError(f"must be str, not {type(a)}"))


def get_missing_ws_info(current_session: Session, save_in_db: bool, station: classes.WeatherStation) -> \
        classes.WeatherStation:
    """ Getting country, numbers weather station, start date of observations, from site rp5.ru."""

    try:
        response = current_session.get(station.link)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        station.number = soup.find("input", id="wmo_id").get('value')
        station.start_date = get_start_date(soup.find("input", id="wmo_id").parent.text)
        country_span = soup.find("div", class_="intoLeftNavi").find("span", class_="verticalBottom")
        for index, child in enumerate(country_span):
            if index == 5:
                station.country = child.find("nobr").text
                break
        station.latitude, station.longitude = \
            get_coordinates(str(soup.find("div", class_="pointNaviCont noprint").find("a")))
        # if save_in_db:
        #     if station.city_id is None:
        #         station.city_id = queries.get_id_from_db()
    return station


def get_text_with_link_on_weather_data_file(current_session: Session, ws_id: int, start_date: date, last_date: date):
    """ Function create query for site rp5.ru with special params for
        getting JS text with link on csv.gz file and returns response of query.
        I use session and headers because site return text - 'Error #FS000;'
        in otherwise.
    """

    current_session.headers = rp5_headers.get_header(current_session.cookies.items()[0][1], 'Chrome')
    try:
        result: Response = current_session.post(
            URL,
            data={'wmo_id': ws_id, 'a_date1': start_date.strftime('%d.%m.%Y'),
                  'a_date2': last_date.strftime('%d.%m.%Y'), 'f_ed3': 3, 'f_ed4': 3, 'f_ed5': 27, 'f_pe': 1,
                  'f_pe1': 2, 'lng_id': 2, })
        return result
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_link_archive_file(text: str) -> str:
    """ Function extract link on archive file with weather data from text."""

    start_position: int = text.find('<a href=http')
    end_position: int = text.find('.csv.gz')
    if start_position > -1 and end_position > -1:
        link: str = text[start_position + 8:end_position + 7]
    else:
        raise ValueError(f'Ссылка на скачивание архива не найдена! Text: "{text}"')
    return link
