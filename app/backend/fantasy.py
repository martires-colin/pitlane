import requests
import json
from database import get_recent_quali, get_session
from models import League, Team

def getFantasyDrivers():
    response = requests.get("http://ergast.com/api/f1/current/drivers.json")
    data = response.json()
    drivers = []
    for i in range(0, int(data['MRData']['total'])):
        drivers.append(data['MRData']['DriverTable']['Drivers'][i]['givenName'] + " " + data['MRData']['DriverTable']['Drivers'][i]['familyName'])
    # print(drivers)
    return drivers

def getFantasyConstructors():
    response = requests.get("http://ergast.com/api/f1/current/constructors.json")
    data = response.json()
    constructors = []
    for i in range(0, int(data['MRData']['total'])):
        constructors.append(data['MRData']['ConstructorTable']['Constructors'][i]['name'])
    # print(drivers)
    return constructors

def getDriverListforWeekend():
    session = get_session()
    quali = get_recent_quali(session)
    print(quali)
    # print(quali.racedid)

def createPointSheet():
    resultsJson = json.load(open("fantasycache/current.json",))
    pointSheet = {"constructors": {}, "drivers": {}}
    for i in range(0, int(resultsJson['MRData']['total'])):
        constructorName = resultsJson['MRData']['RaceTable']['Races'][0]['Results'][i]['Constructor']['constructorId']
        if constructorName in pointSheet['constructors'].keys():
            totalPoints = int(pointSheet['constructors'].get(constructorName)) + int(resultsJson['MRData']['RaceTable']['Races'][0]['Results'][i]['points'])
            pointSheet['constructors'][constructorName] = totalPoints
        else:
            pointSheet['constructors'][constructorName] = resultsJson['MRData']['RaceTable']['Races'][0]['Results'][i]['points']
        driverName = resultsJson['MRData']['RaceTable']['Races'][0]['Results'][i]['Driver']['driverId'] 
        pointSheet['drivers'][driverName] = resultsJson['MRData']['RaceTable']['Races'][0]['Results'][i]['points']
    json.dump(pointSheet, open("fantasycache/pointSheet.json", "w"), indent=4)

def giveScoreForUser(User):
    pointSheet = json.load(open("fantasycache/pointSheet.json",))
    newPoints = int(pointSheet['drivers'].get(User['drivers']['driver1'])) + int(pointSheet['drivers'].get(User['drivers']['driver2'])) + int(pointSheet['constructors'].get(User['constructor'])) + User['totalPoints']
    User['totalPoints'] = newPoints
    return User['totalPoints']

def getUserTeams(User):
    session = get_session()
    teams = session.query(Team).filter(Team.userid == User["userid"])
    session.close()
    return(teams)

def getLeague(leagueID):
    session = get_session()
    teams = []
    leagueName = session.query(League).filter(League.leagueid == leagueID).first()
    for s in session.query(Team).filter(Team.leagueid == leagueID):
        teams.append(s)
    session.close()
    return leagueName, teams

if __name__ == '__main__':
    # createPointSheet()
    User = {
        "name": "Anthony",
        "drivers": {
            "driver1": "hamilton",
            "driver2": "leclerc"
        },
        "constructor": "mercedes",
        "totalPoints": 0,
        "userid": "12345678910",
        "data": {}
    }
    newTotalPoints = giveScoreForUser(User=User)
    User['totalPoints'] = newTotalPoints
    userTeams = getUserTeams(User=User)
    # print(userTeams[0].teamname)
    # print(userTeams[0].leagueid)
    teamLeagues = getLeague(userTeams[0].leagueid)