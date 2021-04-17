Weather parser for site [rp5.ru][1]
========================
About
-------------------------
Parser worked in two modes:
- getting data from the date of start observations;
- getting data for missing period (it is assumed to download from a specific date).

Parser get weather data for your weather stations for years. That data converted for loading to database.
Database structure described in models.py file. Aim of getting weather data might be a lot:
- climate change studies,
- agricaltural expiriments,
- comparison of resort areas, etc...

How to use
-------------------------
Open config.example.ini and write connection to your postgresql database or don't do it if you want to save data in csv files.
Write folder path for saving data it is necessarily. If you want use another database check how to make it with [pyDAL][2].
Parser work with csv file with 3 required parameters:  
- city name (maybe place name);
- link on rp5 site page with that city or place;
- type of data: 0 - weather station, 1 - METAR, 2 - weather sensor;  
and optional parameters (parser add it autonomous):
- last date of download data (yesterday);
- number of weather station;
- country;
- id weather station if you are using database;
- latitude weather station;
- longitude weather station.

[1]: https://rp5.ru/Погода_в_мире "rp5.ru"
[2]: http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer "pyDAL"
