# Python file responsible for site backend implemented by Anthony Ganci
from flask import Flask, jsonify, request
from flask_cors import CORS
# import fastf1
# from fastf1 import plotting
# import io
# import base64
# import numpy as np
import matplotlib as mpl
# from matplotlib import cm
# import matplotlib.pyplot as plt
# from matplotlib.collections import LineCollection
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# import pandas as pd
# from fantasy import *
import warnings
# import requests
# from database import *
# from twilio.rest import Client
# import twilio_config
# from datetime import *
# from datetime import date, datetime
# from dateutil import tz
# import pytz

from .routes import main

# Had to update flask main file to allow for unit testing so all routes are now in routes.py 
def create_app():

    warnings.simplefilter(action='ignore', category=FutureWarning)
    # non-interactive matplotlib backend
    mpl.use('agg')

    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app, resources={r"/*":{'origins':"*"}})
    # app.run(debug=True, host='localhost', port=3001)

    return app
# MOVED ALL OTHER DATABASE FUNCTIONS (and the new create_league and create_team functions to app/backend/database.py)

if __name__ == '__main__':
    create_app()