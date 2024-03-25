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
