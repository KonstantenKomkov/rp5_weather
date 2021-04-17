from datetime import date, datetime, timedelta
from os import listdir, mkdir, path
from requests import Session
import zlib
import configparser


import classes
from db import db
import rp5_parser
import processing
import weather_csv
import queries


config = configparser.ConfigParser()
config.read("config.ini")
DELIMITER = '#'
STATIC_ROOT = config["path"]["static_root"]
SAVE_IN_DB = False if config["db"]["database"] == '' else True


current_session: Session = None


def create_directory(ws: classes.WeatherStation):
    try:
        mkdir(rf"{STATIC_ROOT}{ws.number}")
    except OSError as e:
        # 17 - FileExistsError, folder was created earlier.
        if e.errno != 17:
            raise
        pass


def get_weather_for_year(start_date: date, number: int, ws_id: int):
    """ Function get archive file from site rp5.ru with weather data for one year
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

        answer = rp5_parser.get_text_with_link_on_weather_data_file(current_session, number, start_date, last_date)

        download_link = rp5_parser.get_link_archive_file(answer.text)

        with open(f'{STATIC_ROOT}{number}/{start_date.year}.csv', "wb") as file:
            response = current_session.get(download_link)
            while response.status_code != 200:
                response = current_session.get(download_link)

            # unzip .gz archive
            decompress = zlib.decompress(response.content, wbits=zlib.MAX_WBITS | 16)
            csv_weather_data = decompress.decode('utf-8')

            if SAVE_IN_DB:
                file.write(processing.processing_data(DELIMITER, csv_weather_data.splitlines(), ws_id))
            else:
                file.write(csv_weather_data)
        return True
    elif start_date == yesterday:
        print('Data is actual.')
        return False
    else:
        raise ValueError(f"Query to future {start_date.strftime('%Y.%m.%d')}!")


def get_all_data():
    """ Function get all weather data for all weather stations from csv file
        from start date of observations to today or update data from date of last
        getting weather."""
    global current_session
    wanted_stations = weather_csv.read_new_cities(STATIC_ROOT, DELIMITER)

    if wanted_stations:

        station: classes.WeatherStation
        for station in wanted_stations:

            current_session = Session()

            if station.start_date is None or station.number is None:
                rp5_parser.get_missing_ws_info(current_session, SAVE_IN_DB, station)
                print(f"Start getting data for {station.city} city with "
                      f"start date of observations {station.start_date}...")
            else:
                print(f"Start getting data for {station.city} city with last "
                      f"date of loading {station.start_date.strftime('%Y.%m.%d')} ...")

            create_directory(station)
            start_year: int = station.start_date.year
            if SAVE_IN_DB:
                country_id = db.executesql(queries.get_country_id(station.country))[0][0]
                city_id = db.executesql(queries.get_city_id(station.city, country_id))[0][0]
                station.ws_id = db.executesql(queries.get_ws_id(station, city_id, country_id))[0][0]
                db.commit()
            flag = True
            while start_year < datetime.now().year + 1:
                if start_year == station.start_date.year:
                    start_date: date = station.start_date
                else:
                    start_date: date = date(start_year, 1, 1)
                flag = get_weather_for_year(start_date, station.number, station.ws_id)
                start_year += 1
            station.start_date = datetime.now().date() - timedelta(days=1)
            if flag:
                print("Data was loaded!")
            current_session.close()

    weather_csv.update_csv_file(STATIC_ROOT, DELIMITER, wanted_stations)
    return


def load_data_to_database():
    """ Function check all directories in STATIC_ROOT folder and
        insert data to postgresql database."""
    global STATIC_ROOT
    folders: list = listdir(STATIC_ROOT)

    for folder in folders:
        if path.isdir(f"{STATIC_ROOT}{folder}"):
            for weather_file in listdir(f"{STATIC_ROOT}{folder}"):
                if path.isfile(f"{STATIC_ROOT}{folder}\\{weather_file}") and weather_file[-4:] == '.csv':
                    print(f"Loading weather data for city {folder} at {weather_file[:-4]} year...")
                    try:
                        x = db.executesql(queries.insert_csv_weather_data(
                            f"{STATIC_ROOT}{folder}\\{weather_file}",
                            DELIMITER))
                    except Exception as e:
                        # UniqueViolation, was skipped because all directory will be check
                        if e.pgcode != '23505':
                            print(f"My error: {e.pgcode}")
                            raise
                        pass
                    db.commit()


get_all_data()

# Should be call once before insert data to database
# db.executesql(queries.insert_wind_data)
# db.executesql(queries.insert_cloudiness_data)
# db.executesql(queries.insert_cloudiness_cl_data())
# db.commit()

if SAVE_IN_DB:
    load_data_to_database()
