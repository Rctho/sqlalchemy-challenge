from flask import Flask, jsonify, redirect
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
import datetime as dt
import pandas as pd

#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)


session = Session(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home_page():
   return ("Welcome!<br/>"
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stats from the start date(yyyy-mm-dd): /api/v1.0/date<br/>"
        f"Temperature stats from start to end dates(yyyy-mm-dd): /api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

	rain = session.query(Measurement).all()
	session.close()

	precipitation_dict = []
	for rains in rain:
		year_prcp_dict = {}
		year_prcp_dict["date"] = rains.date
		year_prcp_dict["prcp"] = rains.prcp
		precipitation_dict.append(year_prcp_dict)

	return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.station, Station.name).all()
    session.close()

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2016, 8, 23)
    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()
    session.close()

    temperature_totals = []
    for temps in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperature_totals.append(row)

    return jsonify(temperature_totals)

@app.route("/api/v1.0/<date>")
def from_start_date(date):
    results = session.query(func.min(Measurement.tobs), 
    func.avg(Measurement.tobs), 
    func.max(Measurement.tobs)).\
        filter(Measurement.date >= date).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_results = session.query(func.min(Measurement.tobs), 
    func.avg(Measurement.tobs), 
    func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    return jsonify(multi_results)



if __name__ == "__main__":
    app.run(debug=True)