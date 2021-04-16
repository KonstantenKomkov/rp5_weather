from datetime import date, datetime, timedelta
from os import listdir, mkdir, path
from requests import Session
import zlib


import classes
from db import db
import rp5_parser
import processing
import weather_csv
import queries


DELIMITER = '#'
STATIC_ROOT = './static/'
# False - save csv file to 'city' folder
SAVE_IN_DB = True


current_session: Session = None


def create_directory(ws: classes.WeatherStation):
    try:
        mkdir(rf"{STATIC_ROOT}{ws.city}")
    except OSError as e:
        # 17 - FileExistsError, folder was created earlier.
        if e.errno != 17:
            raise
        pass


def get_weather_for_year(start_date: date, ws_id: int, city: str):
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

        answer = rp5_parser.get_text_with_link_on_weather_data_file(current_session, ws_id, start_date, last_date)

        download_link = rp5_parser.get_link_archive_file(answer.text)

        with open(f'{STATIC_ROOT}{city}/{start_date.year}.csv', "w") as file:
            response = current_session.get(download_link)
            while response.status_code != 200:
                response = current_session.get(download_link)

            # unzip .gz archive
            decompress = zlib.decompress(response.content, wbits=zlib.MAX_WBITS | 16)
            csv_weather_data = decompress.decode('utf-8')

            if SAVE_IN_DB:
                file.write(processing.processing_data(DELIMITER, csv_weather_data.splitlines()))
            else:
                file.write(csv_weather_data)
        return True
    elif start_date == yesterday:
        print('Data is actual.')
        return False
    else:
        raise ValueError(f"Query to future {start_date.strftime('%Y.%m.%d')}!")


def get_all_data_for_weather_stations():
    """ Function get all weather data for all weather stations from csv file
        from start date of observations to today or update data from date of last
        getting weather."""
    global current_session
    wanted_stations = weather_csv.read_new_cities(STATIC_ROOT, DELIMITER)

    if wanted_stations:

        station: classes.WeatherStation
        for station in wanted_stations:

            current_session = Session()

            if station.start_date is None or station.ws_id is None:
                rp5_parser.get_missing_ws_info(current_session, SAVE_IN_DB, station)
                print(f"Start getting data for {station.city} city with "
                      f"start date of observations {station.start_date}...")
            else:
                print(f"Start getting data for {station.city} city with last "
                      f"date of loading {station.start_date.strftime('%Y.%m.%d')} ...")

            create_directory(station)
            start_year: int = station.start_date.year
            # TODO: get_country_id, get_city_id, get_weather_stations_id
            # if SAVE_IN_DB:
            #     country_id = db.executesql(queries.get_country_id(station.country))
            #     if country_id:
            #         station.country
            #     print(country_id)
            #     print(db(get_country_id(station.country)))
            flag = True
            while start_year < datetime.now().year + 1:
                if start_year == station.start_date.year:
                    start_date: date = station.start_date
                else:
                    start_date: date = date(start_year, 1, 1)
                flag = get_weather_for_year(start_date, station.ws_id, station.city)
                start_year += 1
                break
            station.start_date = datetime.now().date() - timedelta(days=1)
            if flag:
                print("Data was loaded!")
            current_session.close()
            break

    weather_csv.update_csv_file(STATIC_ROOT, DELIMITER, wanted_stations)
    return


def load_date_to_database(main_directory):
    """ Function check all directories in STATIC_ROOT folder and
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
#
#     update_or_insert_countries()
#     load_date_to_database(STATIC_ROOT)
# folder = "Казань"
# weather_file = "2005.csv"
# connect_to_database(f"{STATIC_ROOT}{folder}/{weather_file}", DELIMITER)