import classes


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
