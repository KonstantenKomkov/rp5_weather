import classes


def insert_wind_data():
    return "INSERT INTO wind_directions (\"name\") VALUES ('Ветер, дующий с юга'), ('Ветер, дующий с юго-востока'), " \
           "('Ветер, дующий с востока'), ('Штиль, безветрие'), ('Ветер, дующий с юго-юго-востока'), " \
           "('Ветер, дующий с северо-востока'), ('Ветер, дующий с северо-северо-востока'), " \
           "('Ветер, дующий с западо-северо-запада'), ('Ветер, дующий с северо-северо-запада'), " \
           "('Ветер, дующий с востоко-северо-востока'), ('Ветер, дующий с юго-запада'), " \
           "('Ветер, дующий с юго-юго-запада'), ('Ветер, дующий с западо-юго-запада'), ('Ветер, дующий с запада'), " \
           "('Ветер, дующий с северо-запада'), ('Ветер, дующий с севера'), ('Ветер, дующий с востоко-юго-востока'), " \
           "('Переменное направление')"


def insert_cloudiness_data():
    return "INSERT INTO cloudiness (description, scale) VALUES ('Облаков нет', 0), ('10%  или менее, но не 0', 1), " \
           "('20–30', 2), ('40', 3), ('50', 4), ('60', 5), ('70 – 80', 6), ('90  или более, но не 100%', 7), " \
           "('100', 8), ('Небо не видно из-за тумана и/или других метеорологических явлений.', null)"


def insert_cloudiness_cl_data():
    return "INSERT INTO cloudiness_cl (description, scale) VALUES ('Облаков нет', 0), ('10%  или менее, но не 0', 1)," \
           "('20–30', 2), ('40', 3), ('50', 4), ('60', 5), ('70 – 80', 6), ('90  или более, но не 100%', 7), " \
           "('100', 8), ('нет данных', null), " \
           "('Небо не видно из-за тумана и/или других метеорологических явлений.', null)"


def get_country_id(country):
    return "WITH s as (SELECT id, \"name\" FROM countries WHERE \"name\" = '%(country)s'), i as (INSERT INTO " \
           "countries (\"name\") SELECT '%(country)s' WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id " \
           "FROM i UNION ALL SELECT id FROM s" % {'country': country}


def get_city_id(city, country_id):
    return "WITH s as (SELECT id, \"name\", country_id FROM cities WHERE \"name\" = '%(city)s' and country_id = " \
           "%(country_id)i), i as (INSERT INTO cities (\"name\", country_id) SELECT '%(city)s', %(country_id)i " \
           "WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id, \"name\", country_id) SELECT id FROM i UNION ALL " \
           "SELECT id FROM s" % {'city': city, 'country_id': country_id}


def get_ws_id(station: classes.WeatherStation, city_id: int, country_id: int) -> str:
    data_type: str
    if station.data_type == 0:
        data_type = 'метеостанция'
    elif station.data_type == 1:
        data_type = 'METAR'
    else:
        data_type = 'метеодатчик'
    # подумать над station.start_date
    return "WITH s as (SELECT id, \"number\", latitude, longitude, rp5_link, last_date, data_type, city_id, " \
           "country_id FROM weather_stations WHERE \"number\" = %(number)i and rp5_link = '%(link)s' and city_id = " \
           "%(city_id)i and country_id = %(country_id)i and data_type = '%(data_type)s'), i as (INSERT INTO " \
           "weather_stations (\"number\", latitude, longitude, rp5_link, last_date, data_type, city_id, country_id) " \
           "SELECT %(number)i, %(latitude)f, %(longitude)f, '%(link)s', '%(start_date)s', '%(data_type)s', " \
           "%(city_id)i, %(country_id)i WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id, \"number\", latitude, " \
           "longitude, rp5_link, last_date, data_type, city_id, country_id) SELECT id FROM i UNION ALL SELECT id " \
           "FROM s" % {'number': int(station.number), 'link': station.link, 'city_id': city_id,
                       'country_id': country_id, 'data_type': data_type, 'latitude': station.latitude,
                       'longitude': station.longitude, 'start_date': station.start_date}


def insert_csv_weather_data(my_path: str, delimiter: str) -> str:
    return "COPY weather (weather_station_id, \"date\", temperature, pressure, pressure_converted, baric_trend, " \
           "humidity, wind_direction_id, wind_speed, max_wind_speed, max_wind_speed_between, cloud_cover_id, " \
           "current_weather, past_weather, past_weather_two, min_temperature, max_temperature, cloud_cl, " \
           "cloud_count_id, cloud_hight, cloud_cm, cloud_three, visibility, dew_point, rainfall, rainfall_time, " \
           "soil_condition, soil_temperature, soil_with_snow, snow_hight) FROM '%(my_path)s' DELIMITER " \
           "'%(delimiter)s' NULL AS 'null' CSV HEADER;" % {'my_path': my_path, 'delimiter': delimiter}
