import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

@app.route("/")
def home():
    """All available API routes"""
    return ("""
        Available API Routes:<br/>
        '/': Home<br/>
        '/api/v1.0/precipitation': Precipitation data<br/>
        '/api/v1.0/stations': Station data<br/>
        '/api/v1.0/tobs: Temperature data<br/>
        '/api/v1.0/<start>' & '/api/v1.0/<end>': Start and End Dates for temperature data""")

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()
    precipitation_list = []
    for Date, Precipitation in results:
        precip_dict = {}
        precip_dict[Date] = Precipitation
        precipitation_list.append(precip_dict)
    session.close()
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name, Station.id, Station.station, Station.latitude, Station.longitude, Station.elevation).all()
    station_list=[]
    for Name, ID, station, Latitude, Longitude, Elevation in results:
        station_dict = {}
        station_dict['Name'] = Name
        station_dict['ID'] = ID
        station_dict['Station'] = station
        station_dict['Latitude'] = Latitude
        station_dict['Longitude'] = Longitude
        station_dict['Elevation'] = Elevation
        station_list.append(station_dict)
    session.close()
    return jsonify(station_list)




@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(func.max(Measurement.date)).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= (last_date - dt.timedelta(days=365)))

    tobs_list = []
    for Date, Tobs in results:
        tobs_dict = {}
        tobs_dict['Date'] = Date
        tobs_dict['TOBS'] = Tobs
        tobs_list.append(tobs_dict)
    session.close()
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    stats_list = []

    for Minimum, Average, Maximum in results:
        stats_dict = {}
        stats_dict['Minimum'] = Minimum
        stats_dict['Average'] = Average
        stats_dict['Maximum'] = Maximum
        stats_list.append(stats_dict)
    session.close()
    return jsonify(stats_list)

@app.route("/api/v1.0/<start2>")
def start(start2):
    results = results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start2).all()

    stats_list=[]

    for Minimum, Average, Maximum in results:
        stats_dict = {}
        stats_dict['Minimum'] = Minimum
        stats_dict['Average'] = Average
        stats_dict['Maximum'] = Maximum
        stats_list.append(stats_dict)
    session.close()
    return jsonify(stats_list)

if __name__ == "__main__":
    app.run(debug=True)
