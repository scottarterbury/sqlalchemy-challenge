# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my Hawaii Weather API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"For rainfall amounts from 2016-08 to 2017-08:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"For a list of weather stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"For a list of temperatures from our most active weather station:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"For a list of  avg, max, min temps starting from August 2016 in format yyyy-mm-dd:<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"<br/>"
        f"For a list of avg, max, min temps starting from August 2016 to August 2017 in format yyyy-mm-dd/yyyy-mm-dd:<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
  
    # Calculate the date one year from the last date in data set.
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date, prcp in precip:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


# Create second route for stations
"""List of stations to review"""
@app.route("/api/v1.0/stations")
def stations():
    # Create our session from Python to the DB
    session = Session(engine)

    # List the stations and their counts in descending order.
    station_list = session.query(Station.station).\
        order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_list))

    return jsonify(all_stations)


#Create third route for TOBs
"""List of TOBs"""

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session from Python to the DB
    session = Session(engine)

    # List the tobs results
    active_tob = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station=='USC00519281').\
        order_by(Measurement.date).all()

    session.close()
   
    # Convert list of tuples into normal list
    all_tobs = []
    for prcp, date,tobs in active_tob :
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


#Create the fourth route for tobs using the start date
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    # Query tobs for the start date
    starting = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary using the start date from the tobs
    start_date_tobs = []
    for min, avg, max in starting:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 

    return jsonify(start_date_tobs)


#Create the fifth route for tobs using the start and end dates
@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of avg, max, and min tobs for start and end dates"""
    # Query all tobs for date range
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary using the start date and end date and append results
    start_end_tobs = []
    for min, avg, max in start_end:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    
    return jsonify(start_end_tobs)


#Run app
if __name__ == '__main__':
    app.run(debug=True)