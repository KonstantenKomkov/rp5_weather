from datetime import datetime


def processing_data(delimiter: str, csv_weather_data: list, ws_id: int) -> str:
    """ Processing data for database. Check models.py for see database structure."""

    values_line = f'weather_station_id{delimiter} "date"{delimiter} temperature{delimiter} pressure{delimiter} ' \
                  f'pressure_converted{delimiter} baric_trend{delimiter} humidity{delimiter} wind_direction_id' \
                  f'{delimiter} wind_speed{delimiter} max_wind_speed{delimiter} max_wind_speed_between{delimiter} ' \
                  f'cloud_cover_id{delimiter} current_weather{delimiter} past_weather{delimiter} ' \
                  f'past_weather_two{delimiter} min_temperature{delimiter} max_temperature{delimiter} cloud_one' \
                  f'{delimiter} cloud_count_id{delimiter} cloud_hight{delimiter} cloud_two{delimiter} cloud_three' \
                  f'{delimiter} visibility{delimiter} dew_point{delimiter} rainfall{delimiter} rainfall_time' \
                  f'{delimiter} soil_condition{delimiter} soil_temperature{delimiter} soil_with_snow{delimiter} ' \
                  f'snow_hight\n'
    # data from table 'wind_directions'
    wind_direction = ['ветер, дующий с юга', 'ветер, дующий с юго-востока', 'ветер, дующий с востока',
                      'штиль, безветрие', 'ветер, дующий с юго-юго-востока', 'ветер, дующий с северо-востока',
                      'ветер, дующий с северо-северо-востока', 'ветер, дующий с западо-северо-запада',
                      'ветер, дующий с северо-северо-запада', 'ветер, дующий с востоко-северо-востока',
                      'ветер, дующий с юго-запада', 'ветер, дующий с юго-юго-запада',
                      'ветер, дующий с западо-юго-запада', 'ветер, дующий с запада',
                      'ветер, дующий с северо-запада', 'ветер, дующий с севера',
                      'ветер, дующий с востоко-юго-востока', 'переменное направление']
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

        if line_list[6].lower() in wind_direction:
            line_list[6] = wind_direction.index(line_list[6].lower()) + 1
        else:
            line_list[6] = 'null'

        if line_list[21].find('менее ') > -1:
            line_list[21] = line_list[21].replace('менее ', '')

        # incorrect value for pressure
        if line_list[2] != 'null':
            if float(line_list[2]) < 500 or float(line_list[2]) > 900:
                line_list[2] = 'null'

        temp = f'{delimiter}'.join(map(str, line_list))
        values_line = f"{values_line}{ws_id}{delimiter}{temp}\n"

    if values_line[-2:-1] == '\n':
        values_line = values_line[:-2]
    return values_line.encode('utf-8')
