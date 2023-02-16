# Functions for managing the database
# Implemented by Noah Howren unless otherwise stated

from models import Race, Constructor, Constructor_Results, Constructor_Standings, Driver, Driver_Standings, Circuits, Lap_Time, Pit_Stops, Quali, Season, Results, Status, SprintResults, League, Team
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from datetime import date
import string
import random

# Function for creating the session object to connect to the PostgreSQL Database
def get_session():
    engine = create_engine("postgresql://noah-howren:v2_3wcKR_YFyh6PzHaAE6d4Px2YqngLM@db.bit.io/noah-howren/f1_db")
    Session = sessionmaker(bind = engine)
    return Session()

# Function for reteiving current drivers' championship standings.
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
    session.close()
    return standings

# Function for reteiving current constructors' championship standings.
def con_standings():
    session = get_session()
    recentrace = get_recent_race(session)
    standings = {}
    for s in session.query(Constructor_Standings, Constructor).join(Constructor, Constructor.constructorid == Constructor_Standings.constructorid).filter(Constructor_Standings.raceid == recentrace.raceid).order_by(Constructor_Standings.position) :
        x = {'constructor':s.Constructor.name, 'points':s.Constructor_Standings.points}
        standings[s.Constructor_Standings.position] = x
    
    session.close()
    return standings

# Function for returning the most recent Race object in relation to todays date
def get_recent_race(session):
    Date = date.today()
    race = session.query(Race).filter(Race.date <= Date).order_by(desc(Race.date)).first()
    session.close()
    return race

def getRaceForYear(session, year):
    Date = date((year+1),1,1)
    race = session.query(Race).filter(Race.date <= Date).order_by(desc(Race.date)).first()
    session.close()
    return race

# Function for generating an invite code.
# Generates a unique alphanumeric 5 character string for invite code.
def get_invite_code(session):
    code = (''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))
    for x in (session.query(League.invitecode).all()):
        if (x == code):
            return get_invite_code()
        #print(code)
    return code

# Function for creating a league and inserting into db.
# Takes userid of the league creator, and league name. Generates invite code and sets members to onoe.
def create_league(creator, l_name):
    session = get_session()
    league = League(creatorid = creator, name = l_name, invitecode = get_invite_code(session), members = 1)
    session.add(league)
    session.commit()
    session.close()
    return

# Function for creating a league and inserting into db.
# Takes userid, invite code, driver1 id, driver2 id, constructor name, and notification flag
def create_team(u_id, i_code, d1, d2, c_id, t_name, n_f):
    session = get_session()
    l_id = (session.query(League.leagueid).filter(League.invitecode == i_code).first())
    if l_id == None:
        return False
    l_id = l_id[0]
    team = Team(userid = u_id, leagueid = l_id, driver1id = d1, driver2id = d2, constructorid = c_id, teamname = t_name, notifcationflag = n_f)
    session.add(team)
    session.commit()
    session.close()
    return True

# Function for returning all teams in a league,
# Takes leagueID (INTEGER) and returns a LIST of TEAM objects.
def fantasy_info(leagueID):
    return (session.query(Team).filter(Team.leagueid == leagueID).all())


# Function for serializing teams in a league,
# Takes LIST of TEAM objects (see 'fantasy_info(leagueID)') and returns a LIST of DICTIONARIES containing TEAMS DATA.
def fan_drivers_and_constructor(league):
    session = get_session()
    list = []
    for team in league:
        x = ((session.query(Driver.forename, Driver.surname).filter(Driver.driverid == team.driver1id).first()))
        driver1name = x[0] + x[1]
        q = ((session.query(Driver.forename, Driver.surname).filter(Driver.driverid == team.driver2id).first()))
        driver2name = q[0] + q[1]
        constructorname = (session.query(Constructor.name).filter(Constructor.constructorid == team.constructorid).first())[0]
        list.append({"teamname":team.teamname,"points":team.points,"driver1":driver1name, "driver2":driver2name, "constructor":constructorname})
        session.close()
    return list