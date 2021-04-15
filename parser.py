from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import zlib
from os import listdir, path, mkdir
import psycopg2
from pydantic import BaseModel
from requests.exceptions import HTTPError
from requests import Session
from psycopg2 import Error
import rp5


STATIC_ROOT = './static/'
URL = 'https://rp5.ru/responses/reFileSynop.php'
current_session: Session = None
DELIMITER = '#'
# False - save csv file to folder
SAVE_IN_DB = True


class WeatherStation(BaseModel):
    link: str
    ws_id: int = None
    country: str = None
    city_id: int = None
    city: str = None
    latitude: float = None
    longitude: float = None
    start_date: date = None

    def to_csv(self, delimiter):
        # if self.start_date is None:
        #     return f"{self.city}{delimiter}{self.link}{delimiter}{self.city_id}"
        return f"{self.city}{delimiter}{self.link}{delimiter}" \
               f"{'None' if self.start_date is None else self.start_date.strftime('%Y-%m-%d')}" \
               f"{delimiter}{self.ws_id}{delimiter}{self.country}{delimiter}{self.city_id}{delimiter}" \
               f"{self.latitude}{delimiter}{self.longitude}"


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
                    start_date=datetime.strptime(temp[2], '%Y-%m-%d').date() if temp[2] != 'None' else None,
                    ws_id=int(temp[3]) if temp[3] != 'None' else None,
                    country=temp[4] if temp[4] != 'None' else None,
                    city_id=int(temp[5]) if temp[5] != 'None' else None,
                    latitude=temp[6] if temp[6] != 'None' else None,
                    longitude=temp[7] if temp[7] != 'None' else None,))
            else:
                stations.append(WeatherStation(
                    city=temp[0],
                    link=temp[1],))
    return stations


def get_missing_ws_info(station: WeatherStation) -> WeatherStation:
    """Getting start date of observations and numbers weather station from site rp5.ru."""

    global current_session, SAVE_IN_DB

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

    def get_coordinates(a: str) -> tuple[float]:
        if isinstance(a, str):
            if a.find("show_map(") > -1 and a.find(");") > -1 and a.find(", ") > -1:
                temp = a[a.find("show_map(") + 9:a.find(");")].split(", ")
                return float(temp[0]), float(temp[1])
            return None, None
        else:
            raise (TypeError(f"must be str, not {type(a)}"))

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
        country_span = soup.find("div", class_="intoLeftNavi").find("span", class_="verticalBottom")
        for index, child in enumerate(country_span):
            if index == 5:
                station.country = child.find("nobr").text
                break
        print(str(soup.find("div", class_="pointNaviCont noprint").find("a")))
        station.latitude, station.longitude = \
            get_coordinates(str(soup.find("div", class_="pointNaviCont noprint").find("a")))
        # if SAVE_IN_DB:
        #     if station.city_id is None:
        #         station.city_id is = get_id_from_db()
    return station


def create_directory(ws: WeatherStation):
    try:
        mkdir(rf"{STATIC_ROOT}{ws.city}")
    except OSError as e:
        # 17 - FileExistsError, folder was created earlier.
        if e.errno != 17:
            raise
        pass


def get_text_with_link_on_weather_data_file(ws_id: int, start_date: date, last_date: date):
    """Function create query for site rp5.ru with special params for
    getting JS text with link on csv.gz file and returns response of query.
    I use session and headers because site return text - 'Error #FS000;'
    in otherwise."""

    global current_session
    current_session.headers = rp5.get_header(current_session.cookies.items()[0][1], 'Chrome')
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


def processing_data(csv_weather_data: list) -> str:
    """Processing data for database. Check models.py for see database structure."""

    values_line = f'city_id{DELIMITER} "date"{DELIMITER} temperature{DELIMITER} pressure{DELIMITER} ' \
                  f'pressure_converted{DELIMITER} baric_trend{DELIMITER} humidity{DELIMITER} wind_direction_id' \
                  f'{DELIMITER} wind_speed{DELIMITER} max_wind_speed{DELIMITER} max_wind_speed_between{DELIMITER} ' \
                  f'cloud_cover_id{DELIMITER} current_weather{DELIMITER} past_weather{DELIMITER} ' \
                  f'past_weather_two{DELIMITER} min_temperature{DELIMITER} max_temperature{DELIMITER} cloud_one' \
                  f'{DELIMITER} cloud_count_id{DELIMITER} cloud_hight{DELIMITER} cloud_two{DELIMITER} cloud_three' \
                  f'{DELIMITER} visibility{DELIMITER} dew_point{DELIMITER} rainfall{DELIMITER} rainfall_time' \
                  f'{DELIMITER} soil_condition{DELIMITER} soil_temperature{DELIMITER} soil_with_snow{DELIMITER} ' \
                  f'snow_hight\n'
    # data from table 'wind_directions'
    wind_direction = ['Ветер, дующий с юга', 'Ветер, дующий с юго-востока', 'Ветер, дующий с востока',
                      'Штиль, безветрие', 'Ветер, дующий с юго-юго-востока', 'Ветер, дующий с северо-востока',
                      'Ветер, дующий с северо-северо-востока', 'Ветер, дующий с западо-северо-запада',
                      'Ветер, дующий с северо-северо-запада', 'Ветер, дующий с востоко-северо-востока',
                      'Ветер, дующий с юго-запада', 'Ветер, дующий с юго-юго-запада',
                      'Ветер, дующий с западо-юго-запада', 'Ветер, дующий с запада',
                      'Ветер, дующий с северо-запада', 'Ветер, дующий с севера',
                      'Ветер, дующий с востоко-юго-востока']
    # data from table 'cloudiness'
    cloud_cover = ['Облаков нет.', '10%  или менее, но не 0', '20–30', '40', '50', '60',
                   '70 – 80', '90  или более, но не 100%', '100',
                   'Небо не видно из-за тумана и/или других метеорологических явлений.']
    # data from table 'cloudiness_cl'
    count_cloud_cover_nh = ['Облаков нет.', '10%  или менее, но не 0', '20–30', '40', '50', '60',
                            '70 – 80', '90  или более, но не 100%', '100', 'null',
                            'Небо не видно из-за тумана и/или других метеорологических явлений.']

    del csv_weather_data[:7]
    for x in csv_weather_data:
        line_list = x.split('";"')
        line_list[0] = line_list[0][1:-1]
        line_list[-1] = line_list[-1].replace('";', '')

        for i, row in enumerate(line_list):
            if row == '' or row == ' ':
                line_list[i] = 'null'

        line_list[0] = datetime.strptime(line_list[0], '%d.%m.%Y %H:%M')

        if line_list[10] == 'null':
            line_list[10] = 10
        else:
            line_list[10] = cloud_cover.index(line_list[10].replace('%.', '')) + 1
        line_list[17] = count_cloud_cover_nh.index(line_list[17].replace('%.', '')) + 1

        if line_list[6] in wind_direction:
            line_list[6] = wind_direction.index(line_list[6]) + 1

        temp = f'{DELIMITER}'.join(map(str, line_list))
        values_line = f"{values_line}{weather_station_id}{DELIMITER}{temp}\n"

    if values_line[-2:-1] == '\n':
        values_line = values_line[:-2]
    return values_line


def get_weather_for_year(start_date: date, ws_id: int, city: str):
    """Function get archive file from site rp5.ru with weather data for one year
    and save it at directory."""

    global current_session, SAVE_IN_DB
    yesterday = datetime.now().date() - timedelta(days=1)
    if start_date < yesterday:
        if yesterday > date(start_date.year, 12, 31):
            last_date: date = date(start_date.year, 12, 31)
        else:
            # minus one day because not all data for today will be load
            last_date: date = yesterday

        # Cookies might be empty, then get PHPSESSID
        if not current_session.cookies.items():
            current_session.get('https://rp5.ru/')

        answer = get_text_with_link_on_weather_data_file(ws_id, start_date, last_date)

        download_link = get_link_archive_file(answer.text)

        with open(f'{STATIC_ROOT}{city}/{start_date.year}.csv', "w") as file:
            response = current_session.get(download_link)
            while response.status_code != 200:
                response = current_session.get(download_link)

            # unzip .gz archive
            decompress = zlib.decompress(response.content, wbits=zlib.MAX_WBITS | 16)
            csv_weather_data = decompress.decode('utf-8')

            if SAVE_IN_DB:
                file.write(processing_data(csv_weather_data.splitlines()))
            else:
                file.write(csv_weather_data)
        return None
    elif start_date == yesterday:
        print('Data is actual.')
    else:
        raise ValueError(f"Query to future {start_date.strftime('%Y.%m.%d')}!")


def update_csv_file(wanted_stations: [WeatherStation], delimiter):
    """Function update file with our wanted weather stations.
    It write current date and id of weather station."""

    with open(f"{STATIC_ROOT}cities.txt", "w", encoding="utf-8") as csv_file:
        csv_data = ""
        for station in wanted_stations:
            csv_data = f"{csv_data}{station.to_csv(delimiter)}\n"
        csv_file.write(csv_data)


def get_all_data_for_weather_stations():
    """Function get all weather data for all weather stations from csv file
    from start date of observations to today or update data from date of last
    getting weather."""
    global current_session
    wanted_stations = read_new_cities(DELIMITER)

    if wanted_stations:

        station: WeatherStation
        for station in wanted_stations:

            current_session = Session()

            if station.start_date is None or station.ws_id is None:
                get_missing_ws_info(station)
                print(f"Start getting data for {station.city} city with "
                      f"start date of observations {station.start_date}...")
            else:
                print(f"Start getting data for {station.city} city with last "
                      f"date of loading {station.start_date.strftime('%Y.%m.%d')} ...")

            create_directory(station)
            start_year: int = station.start_date.year
            while start_year < datetime.now().year + 1:
                if start_year == station.start_date.year:
                    start_date: date = station.start_date
                else:
                    start_date: date = date(start_year, 1, 1)
                get_weather_for_year(start_date, station.ws_id, station.city)
                start_year += 1
                break
            station.start_date = datetime.now().date() - timedelta(days=1)
            print("Data was loaded!")
            current_session.close()
            break

    update_csv_file(wanted_stations, DELIMITER)
    return


def insert_data_to_datatabase(csv_file_path, delimiter):
    query = "COPY weather (city_id, \"date\", temperature, pressure, pressure_converted, baric_trend, humidity, " \
            "wind_direction_id, wind_speed, max_wind_speed, max_wind_speed_between, cloud_cover_id, current_weather, " \
            "past_weather, past_weather_two, min_temperature, max_temperature, cloud_one, cloud_count_id, cloud_hight, " \
            "cloud_two, cloud_three, visibility, dew_point, rainfall, rainfall_time, soil_condition, soil_temperature, " \
            f"soil_with_snow, snow_hight) FROM '{csv_file_path}' DELIMITER '{delimiter}' NULL AS 'null' CSV HEADER;"
    try:
        # TODO: config file
        connection = psycopg2.connect(
            user="",
            password="",
            host="",
            port="",
            database="")
        cursor = connection.cursor()
        cursor.execute(query)
        # cursor.fetchone()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def load_date_to_database(main_directory):
    """Function check all directories in STATIC_ROOT folder and
    insert data to postgresql database."""
    folders: list = listdir(main_directory)
    for folder in folders:
        if path.isdir(f"{STATIC_ROOT}{folder}"):
            for weather_file in listdir(f"{STATIC_ROOT}{folder}"):
                print(weather_file)
                if path.isfile(f"{STATIC_ROOT}{folder}/{weather_file}") and weather_file[-4:] == '.csv':
                    # TODO: load data to database
                    pass
            break


get_all_data_for_weather_stations()
# if SAVE_IN_DB:
    # load_date_to_database(STATIC_ROOT)
# folder = "Казань"
# weather_file = "2005.csv"
# connect_to_database(f"{STATIC_ROOT}{folder}/{weather_file}", DELIMITER)
