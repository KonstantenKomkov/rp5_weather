from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, null=False, verbose_name='название',)

    class Meta:
        db_table = 'countries'
        verbose_name = 'страна'
        verbose_name_plural = 'страны'


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='страна',)
    name = models.CharField(max_length=50, verbose_name='город',)
    latitude = models.FloatField(verbose_name='широта метеорологической станции',)
    longitude = models.FloatField(verbose_name='долгота метеорологической станции',)

    class Meta:
        db_table = 'cities'
        verbose_name = 'город'
        verbose_name_plural = 'города'


class WindDirection(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='направление ветра (румбы) на высоте 10 - 12 м над земной поверхностью, осреднённое за '
                     '10-минутный период, непосредственно предшествующий сроку наблюдения',)

    class Meta:
        db_table = 'wind_directions'
        verbose_name = 'направление ветра'
        verbose_name_plural = 'направления ветра'


# General cloud cover
class Cloudiness(models.Model):
    description = models.CharField(max_length=100, verbose_name='общая облачность',)
    scale = models.IntegerField(verbose_name='градация', null=True,)

    class Meta:
        db_table = 'cloudiness'
        verbose_name = 'общая облачность'
        verbose_name_plural = 'общая облачность'


# The number of all observed Cl clouds or, in the absence of Cl clouds, the number of all observed Cm clouds
class CloudinessCl(models.Model):
    description = models.CharField(max_length=100, verbose_name='общая облачность', )
    scale = models.IntegerField(verbose_name='градация', null=True,)

    class Meta:
        db_table = 'cloudiness_cl'
        verbose_name = 'процент наблюдающихся облаков'
        verbose_name_plural = 'процент наблюдающихся облаков'


# Data from the weather station
class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='город',)
    date = models.DateTimeField(
        verbose_name='дата и время',)
    temperature = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=1,
        verbose_name='температура воздуха, (°С) на высоте 2 м над поверхностью земли',)
    pressure = models.DecimalField(
        null=True,
        max_digits=4,
        decimal_places=1,
        verbose_name='атмосферное давление на уровне станции (миллиметры ртутного столба)',)
    pressure_converted = models.DecimalField(
        null=True,
        max_digits=4,
        decimal_places=1,
        verbose_name='атмосферное давление, приведённое к среднему уровню моря (миллиметры ртутного столба)',)
    baric_trend = models.DecimalField(
        null=True,
        max_digits=4,
        decimal_places=1,
        verbose_name='барическая тенденция: изменение атмосферного давления за последние 3 часа (миллиметры ртутного '
                     'столба)',)
    humidity = models.IntegerField(
        null=True,
        verbose_name='относительная влажность (%) на высоте 2 м над поверхностью земли',)
    wind_direction = models.ForeignKey(
        WindDirection,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='направление ветра (румбы) на высоте 10 - 12 м над земной поверхностью, осреднённое за '
                     '10-минутный период, непосредственно предшествующий сроку наблюдения',)
    wind_speed = models.IntegerField(
        null=True,
        verbose_name='скорость ветра на высоте 10-12 м над земной поверхностью, осреднённая за 10-минутный период, '
                     'непосредственно предшествующий сроку наблюдения (метры в секунду)',)
    max_wind_speed = models.IntegerField(
        null=True,
        verbose_name='максимальное значение порыва ветра на высоте 10-12 метров над земной поверхностью за 10-минутный '
                     'период, непосредственно предшествующий сроку наблюдения (метры в секунду)',)
    max_wind_speed_between = models.IntegerField(
        null=True,
        verbose_name='максимальное значение порыва ветра на высоте 10-12 метров над земной поверхностью за период '
                     'между сроками (метры в секунду)',)
    cloud_cover = models.ForeignKey(
        Cloudiness,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='общая облачность (%)',)
    current_weather = models.TextField(
        null=True,
        verbose_name='текущая погода, сообщаемая с метеорологической станции',)
    past_weather = models.CharField(
        null=True,
        max_length=255,
        verbose_name='прошедшая погода между сроками наблюдения 1',)
    past_weather_two = models.CharField(
        null=True,
        max_length=255,
        verbose_name='прошедшая погода между сроками наблюдения 2', )
    min_temperature = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=1,
        verbose_name='минимальная температура воздуха (°С) за прошедший период (не более 12 часов)',)
    max_temperature = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        verbose_name='максимальная температура воздуха (°С) за прошедший период (не более 12 часов)', )
    cloud_cl = models.CharField(
        null=True,
        max_length=255,
        verbose_name='слоисто-кучевые, слоистые, кучевые и кучево-дождевые облака (Cl)',)
    cloud_count = models.ForeignKey(
        CloudinessCl,
        on_delete=models.CASCADE,
        verbose_name='количество всех наблюдающихся облаков Cl или, при отсутствии облаков Cl, количество всех '
                     'наблюдающихся облаков Cm',)
    cloud_hight = models.CharField(
        null=True,
        max_length=255,
        verbose_name='высота основания самых низких облаков (м)',)
    cloud_cm = models.CharField(
        null=True,
        max_length=255,
        verbose_name='высококучевые, высокослоистые и слоисто-дождевые облака (Cm)',)
    cloud_three = models.CharField(
        null=True,
        max_length=255,
        verbose_name='перистые, перисто-кучевые и перисто-слоистые облака',)
    visibility = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=1,
        verbose_name='горизонтальная дальность видимости (км)',)
    dew_point = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=1,
        verbose_name='температура точки росы на высоте 2 метра над поверхностью земли (°С)',)
    rainfall = models.CharField(
        null=True,
        max_length=50,
        verbose_name='количество выпавших осадков (мм)',)
    rainfall_time = models.IntegerField(
        null=True,
        verbose_name='период времени за который накоплено указанное количество осадков (часы)',)
    soil_condition = models.CharField(
        null=True,
        max_length=255,
        verbose_name='состояние поверхности почвы без снега или измеримого ледяного покрова',)
    soil_temperature = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=1,
        verbose_name='минимальная температура поверхности почвы за ночь (°С)',)
    soil_with_snow = models.CharField(
        null=True,
        max_length=255,
        verbose_name='состояние поверхности почвы со снегом или измеримым ледяным покровом',)
    snow_hight = models.CharField(
        null=True,
        max_length=255,
        verbose_name='высота снежного покрова (см)',)

    class Meta:
        db_table = 'weather'
        verbose_name = 'погода'
        verbose_name_plural = 'погода'