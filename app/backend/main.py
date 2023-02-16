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
import pandas as pd
from fantasy import *
import warnings
import requests
from database import *
from datetime import date, datetime

warnings.simplefilter(action='ignore', category=FutureWarning)
# non-interactive matplotlib backend
mpl.use('agg')

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
@app.route("/", methods=['GET'])
def index():
    return (jsonify({'status': 200, 'message' :'Welcome to the Pitlane 🏎️'}))

@app.route("/schedule/<int:Year>")
def schedule(Year):
    if request.method == 'GET':
        if Year in range(1950, 2024):
            path = f'https://ergast.com/api/f1/{Year}.json'
            response = requests.get(path)
            jsondump = response.json()
            schedule = []
            for i in range(0, int(jsondump['MRData']['total'])):
                schedule.append((jsondump['MRData']['RaceTable']['Races'][i]['raceName'], jsondump['MRData']['RaceTable']['Races'][i]['date'], jsondump['MRData']['RaceTable']['Races'][i]['time']))
            return(jsonify({'status': 200, 'schedule': schedule, 'season': jsondump['MRData']['RaceTable']['season'] }))

@app.route('/schedule/nextprev', methods=['POST', 'GET'])
def nextprev():
    if request.method == 'POST':

        post_data = request.get_json()
        isOffseason = post_data.get('Offseason')
        if isOffseason:
            lastResponse = requests.get('https://ergast.com/api/f1/current/last.json')
            prevRace = lastResponse.json()['MRData']['RaceTable']['Races'][0]['raceName']
            prevRaceDate = lastResponse.json()['MRData']['RaceTable']['Races'][0]['date']
            # nextSeason = int(response.json()['MRData']['RaceTable']['season']) + 1
            # nextSeasonTable = requests.get(f'https://ergast.com/api/f1/{nextSeason}/1.json')
            nextResponse = requests.get('https://ergast.com/api/f1/current/next.json')
            nextRace = nextResponse.json()['MRData']['RaceTable']['Races'][0]['raceName']
            nextRaceDate = nextResponse.json()['MRData']['RaceTable']['Races'][0]['date']
            
            prevCountryName = lastResponse.json()['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['country']
            nextCountryName = nextResponse.json()['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['country']
            # api for flags is down for some reason
            prevCountry = requests.get(f"https://restcountries.com/v3.1/name/{prevCountryName}?fields=flags")
            prevFlag = prevCountry.json()[0]['flags']['png']
            nextCountry = requests.get(f"https://restcountries.com/v3.1/name/{nextCountryName}?fields=flags")
            nextFlag = nextCountry.json()[0]['flags']['png']
            json.dump({'prevRace': [prevRace, prevRaceDate, prevFlag, prevCountryName], 'nextRace': [nextRace, nextRaceDate, nextFlag, nextCountryName]}, open("fantasycache/NextPrevRaces.json", "w"), indent=4)
            return(jsonify({'status': 200, 'prevRace': [prevRace, prevRaceDate, prevFlag, prevCountryName], 'nextRace': [nextRace, nextRaceDate, nextFlag, nextCountryName]}))
    if request.method == 'GET':
        Date = datetime.today()
        # Date = datetime.strptime("2023-03-21", '%Y-%m-%d')
        # troll = {"currentDate": Date.strftime('%Y-%m-%d')}
        # json.dump(troll, open("fantasycache/NextPrevRaces.json", "w"), indent=4)
        with open("fantasycache/NextPrevRaces.json",'r') as file:
            fileData = json.load(file)
        if Date > datetime.strptime(fileData['currentDate'], '%Y-%m-%d'):
            prevRace, nextRace = getNextPrevRaces(datetime.strptime(fileData['currentDate'], '%Y-%m-%d'))
            prevRace.append(requests.get(f"https://restcountries.com/v3.1/name/{prevRace[2]}?fields=flags").json()[0]['flags']['png'])
            nextRace.append(requests.get(f"https://restcountries.com/v3.1/name/{nextRace[2]}?fields=flags").json()[0]['flags']['png'])
            # print(prevRace, nextRace)
            # print(prevFlag, nextFlag)
            with open("fantasycache/NextPrevRaces.json", "w") as file:
                json.dump({"currentDate": Date.strftime('%Y-%m-%d'), "nextRace": nextRace, "prevRace": prevRace}, file, indent=4)
                
            return jsonify({'status': '200', 'prevRace': prevRace, 'nextRace': nextRace})
        else:
            return jsonify({'status': '200', 'prevRace': fileData['prevRace'], 'nextRace': fileData['nextRace']})


@app.route("/standings/<int:Year>")
def standings(Year):
    if request.method == 'GET':
        if Year in range(1950, 2023):
            standings = getStandings(Year)
            return(jsonify({'standings': standings}))

@app.route("/pitlane", methods=['GET', 'POST'])
def pitlane():
    fastf1.Cache.enable_cache('cache/')
    if request.method == 'POST':
        post_data = request.get_json()
        print(request.get_json())
        if post_data['method'] == 'headtohead':
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
        if post_data['method'] == 'gearshift':
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
        if post_data['method'] == 'speedvisual':
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
@app.route("/fantasy", methods=['GET', 'POST'])
def fantasy():
    # frontend will send userid once that is setup in firebase or our db using psuedo-user for now.
    if request.method == 'POST':
        userID = request.get_json()['userid']
        # print(userID['userid'])
        teams = getUserTeams(userID)
        teamsJSON = []
        for i in range(len(teams.all())):
            teamsJSON.append([teams[i].teamname, teams[i].leagueid])
        return jsonify({'status': '200', 'teams': teamsJSON})

@app.route("/fantasy/league", methods=['POST'])
def fantasyLeague():
    if request.method == 'POST':
        leagueid = request.get_json()['leagueid']
        league = getLeague(leagueid)
        print(league[0])
        return jsonify({'status': '200', 'leagueName': league[0]})


# @app.route("/fantasy/drivers")
# def fantasyDrivers():
#     drivers = getFantasyDrivers()
#     print(drivers)
#     return jsonify({'drivers': drivers})

# @app.route("/fantasy/constructors")
# def fantasyConstructors():
#     constructors = getFantasyConstructors()
#     print(constructors)
#     return jsonify({'constructors': constructors})

# MOVED ALL OTHER DATABASE FUNCTIONS (and the new create_league and create_team functions to app/backend/database.py)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3001)