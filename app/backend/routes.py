from flask import Blueprint, request, jsonify
import requests
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
from .fantasy import *
from .database import *
from datetime import *
from datetime import date, datetime
from dateutil import tz
import pytz
from twilio.rest import Client
from .twilio_config import *
import os

main = Blueprint("main", __name__)

@main.route("/", methods=['GET'])
def index():
    return (jsonify({'status': 200, 'message' :'Welcome to the Pitlane 🏎️'}))

@main.route("/schedule/<int:Year>")
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

@main.route('/schedule/nextprev', methods=['POST', 'GET'])
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

            return(jsonify({'status': 200, 'prevRace': [prevRace, prevRaceDate, prevFlag, prevCountryName], 'nextRace': [nextRace, nextRaceDate, nextFlag, nextCountryName]}))
    if request.method == 'GET':
        # Date = datetime.today()
        # print(get_recent_race().raceid)
        # Date = datetime.strptime("2023-03-21", '%Y-%m-%d')
        # print(Date.today())
        # print(Date.now())
        # print(Date.today())
        # print(datetime.strftime(Date.now(), "%c %z %Z"))
        # t1, t2 = getNextPrevRaces(datetime.strptime("03/05/2023 00:00:00", "%m/%d/%Y %H:%M:%S"))
        # print(t1, t2)

        # troll = {"currentDate": Date.strftime('%Y-%m-%d')}
        # json.dump(troll, open("fantasycache/NextPrevRaces.json", "w"), indent=4)
        with open("fantasycache/NextPrevRaces.json",'r') as file:
            fileData = json.load(file)
        newRecentID = get_recent_race().raceid
        if fileData['recentRaceID'] < newRecentID:
            prevRace, nextRace = getNextPrevRaces(newRecentID)
            # prevRace, nextRace = getNextPrevRaces()
            prevRace.append(requests.get(f"https://restcountries.com/v3.1/name/{prevRace[2]}?fields=flags").json()[0]['flags']['png'])
            nextRace.append(requests.get(f"https://restcountries.com/v3.1/name/{nextRace[2]}?fields=flags").json()[0]['flags']['png'])
            # print(prevRace, nextRace)
            # print(prevFlag, nextFlag)
            with open("fantasycache/NextPrevRaces.json", "w") as file:
                json.dump({"recentRaceID": newRecentID, "nextRace": nextRace, "prevRace": prevRace}, file, indent=4)
                
            return jsonify({'status': '200', 'prevRace': prevRace, 'nextRace': nextRace})
        else:
            return jsonify({'status': '200', 'prevRace': fileData['prevRace'], 'nextRace': fileData['nextRace']})

@main.route("/standings/<int:Year>")
def standings(Year):
    if request.method == 'GET':
        if Year in range(1950, 2024):
            standings = getStandings(Year)
            return(jsonify({'standings': standings}))
        
@main.route("/races/<int:Year>")
def races(Year):
    if request.method == 'GET':
        if Year in range(1950, 2024):
            raceNames = getRaceNamesForYear(Year)
            return (jsonify({'status': '200', 'raceNames': raceNames}))

@main.route("/pitlane", methods=['GET', 'POST'])
def pitlane():
    # fastf1.Cache.enable_cache('cache/')
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
            # can call laps.pick_driver with driver number which we can call from db
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
                'driver': post_data.get('driver1'),
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
@main.route("/fantasy", methods=['GET', 'POST'])
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
    
@main.route("/fantasy/league", methods=['POST', 'PUT'])
def fantasyLeague():
    if request.method == 'POST':
        leagueid = request.get_json()['leagueid']
        userid = request.get_json()['userid']
        league, leaderboard = getLeague(leagueid, userid)
        print(league[0])
        print(leaderboard)
        return jsonify({'status': '200', 'leagueName': league[0], 'leaderboard': leaderboard})
    if request.method == 'PUT':
        data = request.get_json()
        leagueID = data['leagueid']
        newLeaguename = data['newLeaguename']
        updateLeagueName(leagueID, newLeaguename)
        return(jsonify({'status': '200'}))   
@main.route("/fantasy/team", methods=['POST', 'PUT'])
def fantasyTeam():
    if request.method == 'POST':
        userid = request.get_json()['userid']
        leagueid = request.get_json()['leagueid']
        driverRoster, constructorName, points, currentLineup = getTeamJSON(userid, leagueid)
        # teamJSON = getUserTeamJSON(userid, leagueid)
        # print(driverRoster, constructorName, points)
        if len(currentLineup) == 0:
            print({'status': '200', 'driverRoster': driverRoster, 'constructorName': constructorName, 'points': points, 'driver1': driverRoster[0], 'driver2': driverRoster[1]})
        else:    
            return jsonify({'status': '200', 'driverRoster': driverRoster, 'constructorName': constructorName, 'points': points, 'driver1': currentLineup[0], 'driver2': currentLineup[1]})
    if request.method == 'PUT':
        data = request.get_json()
        userid = data['userid']
        leagueID = data['leagueid']
        teamname = data['teamname']
        newTeamname = data['newTeamname']
        updateTeamName(userid, leagueID, teamname, newTeamname)
        return(jsonify({'status': '200'}))    

@main.route("/fantasy/lineup", methods=['POST'])
def fantasyLineup():
    if request.method == 'POST':
        userid = request.get_json()['userid']
        leagueid = request.get_json()['leagueid']
        driver1 = request.get_json()['driver1']
        driver2 = request.get_json()['driver2']
        print(request.get_json())
        fan_update_drivers(userid, leagueid, driver1['driverid'], driver2['driverid'])
        return jsonify({'status': '200'})

@main.route("/fantasy/createLeague", methods=['POST'])
def fantasyCreateLeague():
    if request.method == 'POST':
        userid = request.get_json()['userid']
        leagueName = request.get_json()['leagueName']
        inviteCode = create_league(userid, leagueName)
        return jsonify({'status': '200', 'inviteCode': inviteCode})

@main.route("/fantasy/createTeam", methods=['POST'])
def fantasyCreateTeam():
    if request.method == 'POST':
        # teamInformation
        tInfo = request.get_json()['teamInformation']
        print(tInfo)
        drivers = []
        for index in range(5):
            x = tInfo['roster'][f'd{index+1}'].split()
            # print(x)
            if len(x) > 2:
                x[1] = x[1] + " " + x[2]
                del x[2]
            drivers.append(x)
        print(drivers)    
        roster = driverlist(drivers)
        tInfo['constructorid'] = constructorIDs(tInfo['constructorid'])
        print(tInfo['constructorid'])
        print(roster)
        worked = create_team(u_id=tInfo['userid'], i_code=tInfo['inviteCode'], dr1=roster[0], dr2=roster[1], dr3=roster[2],
                    dr4=roster[3], dr5=roster[4], c_id=tInfo['constructorid'], t_name=tInfo['teamname'], n_f=True) 
        print(worked)
        return jsonify({'status': '200', 'success': worked})
    
@main.route("/fantasy/leagues/<string:uid>", methods=['GET', 'DELETE'])
def fantasyLeagues(uid):
    if request.method == 'GET':
        Page = request.args.get('page', 1, type=int)
        leagues, pageCount = fetchLeagues(uid, Page)
        # leagues = fetchLeagues(uid, Page)
        # print(leagues, pageCount)
        return(jsonify({'status': '200', 'leagues': leagues, 'pages': pageCount}))
    if request.method == 'DELETE':
        data = request.get_json()
        leagueID = data['leagueid']
        # teamname = data['teamname']
        status = deleteLeague(leagueID)
        return(jsonify({'status': status}))
    
@main.route("/fantasy/leagues/<string:uid>/<int:leagueID>", methods=['GET', 'PUT', 'DELETE'])
def viewFantasyLeague(uid, leagueID):
    if request.method == 'GET':
        Name = request.args.get('name', None, type=Boolean)
        TeamName = request.args.get('teamname', None)
        if Name:
            leagueName = fetchLeagueName(leagueID)
            return(jsonify({'status': '200', 'leagueName': leagueName}))
        if TeamName:
            print('Type', type(TeamName))
            print("TeamName:", TeamName)
            teamInfo = fetchManageTeamInfo(leagueID, TeamName)
            print(teamInfo)
            return(jsonify({'status': '200', 'teamInfo': teamInfo}))
        else:
            Page = request.args.get('page', 1, type=int)
            teams, pageCount = fetchLeagueManage(uid, leagueID, Page)
            return(jsonify({'status': '200', 'teams': teams, 'pages': pageCount}))
    if request.method == 'PUT':
        data = request.get_json()
        leagueID = data['leagueid']
        teamname = data['teamname']
        updatedInfo = data['updatedInfo']
        print(updatedInfo)
        updateTeamInfo(leagueID, teamname, updatedInfo)
        return(jsonify({'status': '200'}))
    if request.method == 'DELETE':
        data = request.get_json()
        leagueID = data['leagueid']
        teamname = data['teamname']
        deleteTeam(leagueID, teamname)
        return(jsonify({'status': '200'}))

# Ideally want to combine these two and check firebase to see if user is admin 
@main.route("/admin/leagues/", methods=['GET'])
def adminLeagues():
    if request.method == 'GET':
        Page = request.args.get('page', 1, type=int)
        leagues, pageCount = fetchLeaguesAdmin(Page)
        return(jsonify({'status': '200', 'leagues': leagues, 'pages': pageCount}))
        # return(jsonify({'status': '200'}))
# @main.route("/fantasy/constructors")
# def fantasyConstructors():
#     constructors = getFantasyConstructors()
#     print(constructors)
#     return jsonify({'constructors': constructors})
# @main.route("/fantasy/team", methods=['GET', 'POST'])
# @main.route("/fantasy/drivers")
# def fantasyDrivers():
#     drivers = getFantasyDrivers()
#     print(drivers)
#     return jsonify({'drivers': drivers})


# Colin Martires - push notifications via Twilio
@main.route("/send_SMS", methods=['POST'])
def sendSMS():
    post_data = request.get_json()
    user_phone_number = post_data['phoneNumber']
    msg_body = post_data['msg_body']

    # Twilio Client to handle SMS notifications
    print("SENDING SMS via TWILIO")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body=msg_body,
    from_=twilio_number,
    to=user_phone_number
    )

    return jsonify({
        'status': "success",
        'message_sid': message.sid
    })

# Colin Martires - retrieve race results from database
# notif_res() by Noah Howren
@main.route("/race_results_notif", methods=["GET"])
def getRaceResultsNotif():
    msg_body = ''
    recent_race = get_recent_race().name
    data = notif_res()

    msg_body += f'PITLANE\n\nRace Results for {recent_race}\n'
    for x in data["Results"]:
        msg_body += f'{str(x["Position"]).ljust(3)} {x["Driver"]}\n'

    return(jsonify({
        'results': data,
        'msg_body': msg_body
    }))

# Colin Martires - retreive driver standings from database
# notif_res() by Noah Howren
@main.route("/driver_standings_notif", methods=["GET"])
def getDriverStandingsNotif():
    msg_body = ''
    data = notif_res()

    msg_body += "PITLANE\n\nDriver's Championship Standings\n"
    for y in data["Standings"]:
        msg_body += f'{str(y["Position"]).ljust(3)} {y["Driver"].ljust(17)} {int(y["Points"])}pts\n'

    return(jsonify({
        'results': data,
        'msg_body': msg_body
    }))

# Colin Martires - retreive constructor standings from database
# notif_res() by Noah Howren
@main.route("/constructor_standings_notif", methods=["GET"])
def getConstructorStandingsNotif():
    msg_body = ''
    data = notif_res()

    msg_body += "PITLANE\n\nConstructor's Championship Standings\n"
    for z in data["Constructors"]:
        if z["Constructor"] == "Williams":
            msg_body += f'{str(z["Position"]).ljust(3)} WilliamsRacing {int(z["Points"])}pts\n'
        else:
            msg_body += f'{str(z["Position"]).ljust(3)} {z["Constructor"].ljust(12)} {int(z["Points"])}pts\n'

    return(jsonify({
        'results': data,
        'msg_body': msg_body
    }))

# Colin Martires - retreive upcoming race from database
# upcoming_race() by Noah Howren
@main.route("/upcoming_race_notif", methods=["GET"])
def getUpcomingRaceNotif():
    msg_body = ''
    data = upcoming_race()

    race_name = data["Race"]
    date_time_str = data["Date"]

    date_time_format = "%m-%d-%Y %H:%M:%S"
    date_time_obj = datetime.strptime(date_time_str, date_time_format)
    d_utc = date_time_obj.replace(tzinfo=tz.tzutc())
    d_pst = d_utc.astimezone(tz.tzlocal())
    race_time_formatted = d_pst.time().strftime("%I:%M %p")
    race_date = date_time_obj.date().strftime("%m-%d-%Y")

    msg_body = f"PITLANE\n\nUpcoming Race\n{race_name}\nDate: {race_date}\nTime: {race_time_formatted} PST"

    return(jsonify({
        'results': data,
        'msg_body': msg_body
    }))

# Colin Martires - send notification 15 mins before race start
# is_lights_out() by Noah Howren
@main.route("/lights_out_notif", methods=["GET"])
def getLightsOutNotif():
    msg_body = ''
    data = is_lights_out()

    # commented out for demo
    # if data['status']:
    #     msg_body = f"PITLANE\n\nThe {data['Race']} starts in 15 minutes!"
    #     return(jsonify({
    #         'results': data['status'],
    #         'msg_body': msg_body
    #     }))

    # return(jsonify({
    #     'results': data['status'],
    #     'msg_body': msg_body
    # }))

    # simulated response
    msg_body = f"PITLANE\n\nThe Bahrain Grand Prix starts in 15 minutes!"

    return(jsonify({
        'results': True,
        'msg_body': msg_body
    }))