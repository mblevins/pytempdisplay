#
import json
from datetime import datetime
from datetime import timedelta
import pytz
import requests
from flask import Flask
from flask import request
from flask import render_template
from flask_apscheduler import APScheduler
import logging

class Config(object):
    SCHEDULER_API_ENABLED = True
    STATION_URL = None

station_data={
    "date": "2020-01-01T00:00+00:00",
    "temp": 0.0,
    "humidity": 0.0,
    "rainrate": 0.0,
    "raintotal": 0.0}

poll_time_seconds=300
allow_seconds_skew=900

app = Flask(__name__)
app.config.from_object(Config())
app.config.from_envvar("PYTEMP_CONFIG")
scheduler = APScheduler()

@app.route('/stationData')
def hello_world():
    log = logging.getLogger(__name__)
    format=request.headers['Accept']
    log.debug(f"format={format}")
    if (format == "Application/json"):
        return json.dumps(station_data)
    else:
        color="green"
        skew=datetime.now(tz=pytz.timezone("America/Los_Angeles")) - datetime.fromisoformat(station_data["date"])
        log.debug(f"skew={skew}")
        if (skew > timedelta(seconds=allow_seconds_skew)):
            color="red"
        temp=int(round(station_data["temp"],0))
        return render_template(
            'small-temp.html',
            temp=temp,
            color=color)

@scheduler.task('interval', id='poll_station', seconds=poll_time_seconds)
def pollStation():
    global station_data
    log = logging.getLogger(__name__)
    # See https://www.meteobridge.com/wiki/index.php/Add-On_Services
    r = requests.get(app.config["STATION_URL"])
    for line in r.text.split('\n'):
        fields=line.split(' ')
        if (len(fields) > 2):
            if (fields[1] == "th0"):
                d = fields[0]
                idate=datetime(int(d[0:4]),int(d[4:6]),int(d[6:8]),int(d[8:10]),int(d[10:12]),int(d[12:14]),tzinfo=pytz.timezone("UTC"))
                station_data["date"] = idate.astimezone(pytz.timezone("America/Los_Angeles")).isoformat()
                station_data["temp"] = round(float(fields[2])*1.8+32,1)
                station_data["humidity"] = fields[3]
            elif (fields[1] == "rain0"):
                station_data["rainrate"] = round(float(fields[2])*25.4,2)
                station_data["raintotal"] = round(float(fields[2])*25.4,2)

    log.debug(json.dumps(station_data,indent=4))


# init
loglevel=logging.ERROR
if (app.config["DEBUG"]):
    loglevel=logging.DEBUG

logging.basicConfig(level=loglevel,
    format='%(asctime)s %(levelname)s %(message)s')

scheduler.start()
pollStation()

if __name__ == "__main__":
    app.run()
