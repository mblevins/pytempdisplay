web server to fetch temperature, display in html or json, and optionally upload to cloud

See https://www.meteobridge.com/wiki/index.php/Add-On_Services for station API used

to test

```
export PYTEMP_CONFIG=config/pytemp-dev.cfg
python3 ./station-server.py
curl http://localhost:5000/stationData
```


to run

```
export PYTEMP_CONFIG=config/pytemp-prod.cfg
gunicorn -w 4 station-server:app
curl http://localhost:8000/stationData
```


When committing,

```
pip freeze > requirements.txt
```
