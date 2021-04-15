from datetime import datetime


def processing_data(delimiter: str, csv_weather_data: list) -> str:
    """ Processing data for database. Check models.py for see database structure."""

    values_line = f'city_id{delimiter} "date"{delimiter} temperature{delimiter} pressure{delimiter} ' \
                  f'pressure_converted{delimiter} baric_trend{delimiter} humidity{delimiter} wind_direction_id' \
                  f'{delimiter} wind_speed{delimiter} max_wind_speed{delimiter} max_wind_speed_between{delimiter} ' \
                  f'cloud_cover_id{delimiter} current_weather{delimiter} past_weather{delimiter} ' \
                  f'past_weather_two{delimiter} min_temperature{delimiter} max_temperature{delimiter} cloud_one' \
                  f'{delimiter} cloud_count_id{delimiter} cloud_hight{delimiter} cloud_two{delimiter} cloud_three' \
                  f'{delimiter} visibility{delimiter} dew_point{delimiter} rainfall{delimiter} rainfall_time' \
                  f'{delimiter} soil_condition{delimiter} soil_temperature{delimiter} soil_with_snow{delimiter} ' \
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

        temp = f'{delimiter}'.join(map(str, line_list))
        # {weather_station_id}
        values_line = f"{values_line}1{delimiter}{temp}\n"

    if values_line[-2:-1] == '\n':
        values_line = values_line[:-2]
    return values_line
