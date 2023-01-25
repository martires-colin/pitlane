# Python file responsible for site backend implemented by Anthony Ganci
from flask import Flask, jsonify, request
from flask_cors import CORS
import fastf1
from fastf1 import plotting
import io
import base64
import numpy as np
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, desc, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date
import json
import pandas as pd
from models import Race, Constructor, Constructor_Results, Constructor_Standings, Driver, Driver_Standings, Circuits, Lap_Time, Pit_Stops, Quali, Season, Results, Status, SprintResults
import warnings
import requests

warnings.simplefilter(action='ignore', category=FutureWarning)
# non-interactive matplotlib backend
mpl.use('agg')

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
@app.route("/", methods=['GET'])
def index():
    return (jsonify({'status': 200, 'message' :'Welcome to the Pitlane 🏎️'}))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        post_data = request.get_json()
        year = post_data.get('season')
        path = f'https://ergast.com/api/f1/{year}.json'
        response = requests.get(path)
        jsondump = response.json()
        schedule = []
        for i in range(0, int(jsondump['MRData']['total'])):
            schedule.append((jsondump['MRData']['RaceTable']['Races'][i]['raceName'], jsondump['MRData']['RaceTable']['Races'][i]['date'], jsondump['MRData']['RaceTable']['Races'][i]['time']))
        return(jsonify({'status': 200, 'schedule': schedule, 'season': jsondump['MRData']['RaceTable']['season'] }))
    if request.method == 'GET':
        # year = request.headers['year']
        body = request.get_json()
        year = body.get('season')
        path = f'https://ergast.com/api/f1/{year}.json'
        response = requests.get(path)
        jsondump = response.json()
        schedule = []
        for i in range(0, int(jsondump['MRData']['total'])):
            schedule.append((jsondump['MRData']['RaceTable']['Races'][i]['raceName'], jsondump['MRData']['RaceTable']['Races'][i]['date'], jsondump['MRData']['RaceTable']['Races'][i]['time']))
        return(jsonify({'status': 200, 'schedule': schedule, 'season': jsondump['MRData']['RaceTable']['season']}))

@app.route('/schedule/nextprev', methods=['POST'])
def nextprev():
    if request.method == 'POST':
        post_data = request.get_json()
        isOffseason = post_data.get('Offseason')
        if isOffseason:
            response = requests.get('https://ergast.com/api/f1/current.json')
            total = int(response.json()['MRData']['total'])-1
            prevRace = response.json()['MRData']['RaceTable']['Races'][total]['raceName']
            prevRaceDate = response.json()['MRData']['RaceTable']['Races'][total]['date']
            prevRaceID = f"/track/{response.json()['MRData']['RaceTable']['Races'][total]['Circuit']['circuitId']}"
            nextSeason = int(response.json()['MRData']['RaceTable']['season']) + 1
            nextSeasonTable = requests.get(f'https://ergast.com/api/f1/{nextSeason}/1.json')
            nextRace = nextSeasonTable.json()['MRData']['RaceTable']['Races'][0]['raceName']
            nextRaceDate = nextSeasonTable.json()['MRData']['RaceTable']['Races'][0]['date']
            nextRaceID = f"/track/{nextSeasonTable.json()['MRData']['RaceTable']['Races'][0]['Circuit']['circuitId']}"
            print(nextRaceID, prevRaceID)
            prevCountry = requests.get(f"https://restcountries.com/v3.1/name/{response.json()['MRData']['RaceTable']['Races'][total]['Circuit']['Location']['country']}?fields=flags")
            prevFlag = prevCountry.json()[0]['flags']['png']
            nextCountry = requests.get(f"https://restcountries.com/v3.1/name/{nextSeasonTable.json()['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['country']}?fields=flags")
            nextFlag = nextCountry.json()[0]['flags']['png']
            # prevFlag = ""
            # print(prevCountry.json()[0]['flags']['png'])
            return(jsonify({'status': 200, 'prevRace': [prevRace, prevRaceDate, prevFlag], 'nextRace': [nextRace, nextRaceDate, nextFlag]}))

@app.route("/standings", methods=['GET', 'POST'])
def standings():
    if request.method == 'GET':
        standings = getStandings(0)
        return(jsonify({'status': 200, 'drivers': standings}))
    if request.method == 'POST':
        post_data = request.get_json()
        standings = getStandings(int(post_data.get('year')))
        return(jsonify({'status': 200, 'standings': standings}))

@app.route("/pitlane", methods=['GET', 'POST'])
def pitlane():
    fastf1.Cache.enable_cache('cache/')
    if request.method == 'POST':
        post_data = request.get_json()['form']
        print(request.get_json())
        if post_data['method'] == 'h2h':
            # data dictionary for the form data retreived
            DATA = {'driver1': '', 'driver2': '', 'track': '', 'year': 0, 'session' : ''}
            DATA.update({
                'driver1': post_data.get('driver1'),
                'driver2': post_data.get('driver2'),
                'track': post_data.get('track'),
                'year': int(post_data.get('year')),
                'session': post_data.get('session')
            })
            plotting.setup_mpl()
            race = fastf1.get_session(DATA['year'], DATA['track'], DATA['session'])
            race.load()

            driver1Name = race.get_driver(DATA['driver1'])['LastName']
            driver2Name = race.get_driver(DATA['driver2'])['LastName']
            driver1 = race.laps.pick_driver(DATA['driver1'])
            driver2 = race.laps.pick_driver(DATA['driver2'])
            driver1Color = plotting.driver_color(DATA['driver1'])
            driver2Color = plotting.driver_color(DATA['driver2'])

            # Based on information given by FastF1 documentation on how to do basic plotting
            fig, ax = plt.subplots(figsize=(10, 6.75))
            title = plt.suptitle(
                f"Driver Head-to-Head\n"
                f"{race.event['EventName']} {race.event.year}\n"
                f"{driver1Name} vs. {driver2Name}")
            line1, = ax.plot(driver1['LapNumber'], driver1['LapTime'], color=driver1Color, label=driver1Name)
            line2, = ax.plot(driver2['LapNumber'], driver2['LapTime'], color=driver2Color, label=driver2Name)
            # ax.set_title(f"{driver1Name} vs. {driver2Name}")
            ax.set_xlabel("Lap Number")
            ax.set_ylabel("Lap Time")
            ax.legend(handles=[line1, line2])
            
            # converting matplotlib image to base64 so i can display it easy
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return jsonify({'src': pngImageB64String, 'status': 'success'})
        if post_data['method'] == 'gear':
            # data dictionary for the form data retreived
            DATA = {'track': '', 'year': 0, 'session' : ''}
            DATA.update({
                'track': post_data.get('track'),
                'year': int(post_data.get('year')),
                'session': post_data.get('session')
            })
            plotting.setup_mpl()

            session = fastf1.get_session(DATA['year'], DATA['track'], DATA['session'])
            session.load()

            lap = session.laps.pick_fastest()
            lastname = session.get_driver(lap['Driver'])['LastName']

            # Based on information given by FastF1 documentation on how to do basic plotting
            tel = lap.get_telemetry()

            x = np.array(tel['X'].values)
            y = np.array(tel['Y'].values)

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            gear = tel['nGear'].to_numpy().astype(float)

            fig = plt.figure(figsize=(10, 6.75))
            # cmap = cm.get_cmap('gnuplot', 8)
            cmap = cm.get_cmap('plasma', 8)
            lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
            lc_comp.set_array(gear)
            lc_comp.set_linewidth(4)

            plt.gca().add_collection(lc_comp)
            plt.axis('equal')
            plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

            title = plt.suptitle(
                f"Fastest Lap Gear Shift\n"
                f"{lastname} - {session.event['EventName']} {session.event.year}"
            )

            cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
            cbar.set_ticks(np.arange(1.5, 9.5))
            cbar.set_ticklabels(np.arange(1, 9))

            # converting matplotlib image to base64 so i can display it easy
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return jsonify({'src': pngImageB64String, 'status': 'success'})
        if post_data['method'] == 'speed':
            # data dictionary for the form data retreived
            DATA = {'driver': '', 'track': '', 'year': 0, 'session' : ''}
            DATA.update({
                'driver': post_data.get('driver'),
                'track': post_data.get('track'),
                'year': int(post_data.get('year')),
                'session': post_data.get('session')
            })
            
            plotting.setup_mpl()
            session = fastf1.get_session(DATA['year'], DATA['track'], DATA['session'])
            session.load()
            lap = session.laps.pick_driver(DATA['driver']).pick_fastest()
            lastname = session.get_driver(lap['Driver'])['LastName']
            colormap = mpl.cm.plasma
            
            # Based on information given by FastF1 documentation on how to do basic plotting
            x = lap.telemetry['X']              
            y = lap.telemetry['Y']              
            color = lap.telemetry['Speed']      

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(10, 6.75))
            title = plt.suptitle(
                f"Fastest Lap Speed Visualization\n"
                f"{lastname} - {session.event['EventName']} {session.event.year}\n"
            )
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
            ax.axis('off')
            ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)
            norm = plt.Normalize(color.min(), color.max())
            lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)
            lc.set_array(color)
            line = ax.add_collection(lc)
            cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
            normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
            legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")
            
            # converting matplotlib image to base64 so i can display it easy
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return jsonify({'src': pngImageB64String, 'status': 'success'})

    if request.method == 'GET':    
        # return jsonify({'msg': "Welcome to Pitlane 🏎️! Enter information to get started!", 'status': 'success'})
        return jsonify({'status': 'success'})

# Function for reteiving current drivers' championship standings.
# Noah Howren
def getStandings(year):
    session = get_session()
    if year == 0:
        recentrace = get_recent_race(session)
    else:
        recentrace = getRaceForYear(session, year)
    standings = []
    for s in session.query(Driver_Standings, Driver).join(Driver, Driver.driverid == Driver_Standings.driverid).filter(Driver_Standings.raceid == recentrace.raceid).order_by(Driver_Standings.position) :
        # x = {'driver':(s.Driver.forename + ' ' + s.Driver.surname), 'points':s.Driver_Standings.points}
        # standings[s.Driver_Standings.position] = x
        standings.append((s.Driver_Standings.position, s.Driver.forename + ' ' + s.Driver.surname, s.Driver_Standings.points))
    return standings

# Function for reteiving current constructors' championship standings.
# Noah Howren
def con_standings():
    session = get_session()
    recentrace = get_recent_race(session)
    standings = {}
    for s in session.query(Constructor_Standings, Constructor).join(Constructor, Constructor.constructorid == Constructor_Standings.constructorid).filter(Constructor_Standings.raceid == recentrace.raceid).order_by(Constructor_Standings.position) :
        x = {'constructor':s.Constructor.name, 'points':s.Constructor_Standings.points}
        standings[s.Constructor_Standings.position] = x
    return standings

# Function for creating the session object to connect to the PostgreSQL Database
# Noah Howren
def get_session():
    engine = create_engine("postgresql://noah-howren:v2_3wcKR_YFyh6PzHaAE6d4Px2YqngLM@db.bit.io/noah-howren/f1_db")
    Session = sessionmaker(bind = engine)
    return Session()

# Function for returning the most recent Race object in relation to todays date
# Noah Howren
def get_recent_race(session):
    Date = date.today()
    race = session.query(Race).filter(Race.date <= Date).order_by(desc(Race.date)).first()
    return race

def getRaceForYear(session, year):
    Date = date((year+1),1,1)
    race = session.query(Race).filter(Race.date <= Date).order_by(desc(Race.date)).first()
    return race

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3001)