import requests
import json
from database import *
from models import *
from sqlalchemy import asc, desc

def driverlist(fn, sn):
    session = get_session()
    q = session.query(Driver).filter(Driver.forename==fn, Driver.surname==sn).first()
    session.close()
    return(q.driverid)

def constructorIDs(constructorName):
    session = get_session()
    q = session.query(Constructor).filter(Constructor.name == constructorName).first()
    session.close()
    return(q.constructorid)

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
    json.dump(pointSheet, open("fantasycache/raceResults.json", "w"), indent=4)

def giveScoreForUser(User):
    pointSheet = json.load(open("fantasycache/raceResults.json",))
    newPoints = int(pointSheet['drivers'].get(User['drivers']['driver1'])) + int(pointSheet['drivers'].get(User['drivers']['driver2'])) + int(pointSheet['constructors'].get(User['constructor'])) + User['totalPoints']
    User['totalPoints'] = newPoints
    return User['totalPoints']

def getUserTeams(userid):
    session = get_session()
    teams = session.query(Team).filter(Team.userid == userid)
    session.close()
    for i in range(len(teams.all())):
        print(teams[i].teamname)
    return(teams)

# Replaced by function in db.py
# def getUserTeamJSON(userid, leagueid):
#     session = get_session()
#     team = session.query(Team).filter(Team.userid == userid, Team.leagueid == leagueid).first()
#     session.close()
#     # make a json file with driverid -> driver name and constructorid -> constructor name
#     teamJSON = {'driver1id': team.driver1id, 'driver2id': team.driver2id, 'constructorid': team.constructorid, 'points': team.points}
#     return teamJSON

def getLeague(leagueID):
    session = get_session()
    teams = []
    leagueName = session.query(League).filter(League.leagueid == leagueID).first().name
    for s in session.query(Team).filter(Team.leagueid == leagueID):
        teams.append(s)
    session.close()
    return leagueName, teams

def getNextPrevRaces(Date):
    session = get_session()
    nextRace = session.query(Race).filter(Race.date >= Date).order_by(asc(Race.date)).first()
    # nextRace = session.query(Race).filter(Race.date >= Date).first()
    # print(nextRace.year, nextRace.round, nextRace.name)
    if nextRace.round == 1:
        prevRace = session.query(Race).filter(Race.year == nextRace.year-1).order_by(desc(Race.round)).first()
        # print(prevRace.year, prevRace.round, prevRace.name)
    else:
        prevRace = session.query(Race).filter(Race.year == nextRace.year, Race.round == nextRace.round-1).first()
        # print(prevRace.year, prevRace.round, prevRace.name)
    prevRaceCountry = session.query(Circuits).filter(Circuits.circuitid == prevRace.circuitid).first()
    nextRaceCountry = session.query(Circuits).filter(Circuits.circuitid == nextRace.circuitid).first()
    session.close()   
    return [prevRace.name, prevRace.date.strftime('%Y-%m-%d'), prevRaceCountry.country], [nextRace.name, nextRace.date.strftime('%Y-%m-%d'), nextRaceCountry.country]

# if __name__ == '__main__':
    # createPointSheet()
    # User = {
    #     "name": "Anthony",
    #     "drivers": {
    #         "driver1": "hamilton",
    #         "driver2": "leclerc"
    #     },
    #     "constructor": "mercedes",
    #     "totalPoints": 0
    # }
    # giveScoreForUser(User=User)