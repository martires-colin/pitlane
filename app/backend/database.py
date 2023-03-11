# Functions for managing the database
# Implemented by Noah Howren unless otherwise stated

from .models import Race, Constructor, Constructor_Results, Constructor_Standings, Driver, Driver_Standings, Circuits, Lap_Time, Pit_Stops, Quali, Season, Results, Status, SprintResults, League, Team
from sqlalchemy import create_engine, desc, update
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime, timedelta
import string
import random

def getRaceNamesForYear(year):
    session = get_session()
    list = []
    for q in session.query(Race.name).filter(Race.year == year).all():
        list.append(q.name)
    session.close()
    return list

# Function for creating the session object to connect to the PostgreSQL Database
def get_session():
    engine = create_engine("postgresql://noah-howren:v2_3wcKR_YFyh6PzHaAE6d4Px2YqngLM@db.bit.io/noah-howren/f1_db")
    Session = sessionmaker(bind = engine)
    return Session()

# Function for reteiving current drivers' championship standings.
def getStandings(year):
    session = get_session()
    if year == datetime.utcnow().year:
        recentrace = get_recent_race()
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
    recentrace = get_recent_race()
    standings = {}
    for s in session.query(Constructor_Standings, Constructor).join(Constructor, Constructor.constructorid == Constructor_Standings.constructorid).filter(Constructor_Standings.raceid == recentrace.raceid).order_by(Constructor_Standings.position) :
        x = {'constructor':s.Constructor.name, 'points':s.Constructor_Standings.points}
        standings[s.Constructor_Standings.position] = x
    
    session.close()
    return standings

# Function for returning the most recent Race object in relation to todays date
def get_recent_race():
    session = get_session()
    Date = datetime.utcnow()
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
    invCode = get_invite_code(session)
    league = League(creatorid = creator, name = l_name, invitecode = invCode, members = 0)
    session.add(league)
    session.commit()
    session.close()
    return invCode

# Function for creating a league and inserting into db.
# Takes userid, invite code, driver1 id, driver2 id, constructor name, and notification flag
def create_team(u_id, i_code, dr1, dr2, dr3, dr4, dr5, c_id, t_name, n_f):
    session = get_session()
    l = (session.query(League).filter(League.invitecode == i_code).first())
    if League == None:
        return False
    l_id = l.leagueid
    session.execute(update(League).where(League.leagueid == l_id).values(members = l.members + 1)) 
    team = Team(userid = u_id, leagueid = l_id, d1 = dr1, d2 = dr2, d3 = dr3, d4 = dr4, d5 = dr5, 
                constructorid = c_id, teamname = t_name, notifcationflag = n_f, points=0, driver1id=dr1, driver2id=dr2)
    session.add(team)
    session.commit()
    session.close()
    return True

# Function for returning all teams in a league,
# Takes leagueID (INTEGER) and returns a LIST of TEAM objects.
def fantasy_info(leagueID, session):
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
        list.append({"teamname":team.teamname,"points":team.points,"driver1":driver1name,"driver2":driver2name,"constructor":constructorname})
    session.close()
    return list

def getTeamJSON(userid, leagueid):
    session = get_session()
    subquery = (session.query(Team.d1, Team.d2, Team.d3, Team.d4, Team.d5).filter(Team.userid == userid).first())
    q = (session.query(Driver.driverid, Driver.forename, Driver.surname).filter(Driver.driverid.in_(subquery)).all())
    roster = []
    for x in q:
        roster.append({'drivername':x[1] + ' ' + x[2], 'driverid': x[0]})
    constructorid = session.query(Team.constructorid).filter(Team.userid == userid, Team.leagueid == leagueid).first()
    constructorName = session.query(Constructor.name).filter(Constructor.constructorid == constructorid[0]).first()
    points = session.query(Team.points).filter(Team.userid == userid, Team.leagueid == leagueid).first()
    currentDrivers = session.query(Team.driver1id, Team.driver2id).filter(Team.userid == userid, Team.leagueid == leagueid).first()
    curDrivers = session.query(Driver.driverid, Driver.forename, Driver.surname).filter(Driver.driverid.in_(currentDrivers)).all()
    curLineup = []
    for x in curDrivers:
        curLineup.append({'drivername': x[1] + ' ' + x[2], 'driverid': x[0]})
    session.close()
    return roster, {'constructorid': constructorid[0], 'constructorName': constructorName[0]}, points[0], curLineup

def fan_update_drivers(userid, leagueid, d1, d2):
    session = get_session()
    session.execute(update(Team).where(Team.userid == userid, Team.leagueid == leagueid).values(driver1id=d1, driver2id = d2))
    session.commit()
    session.close()

def notif_res():
    session = get_session()
    now = datetime.utcnow()
    race = session.query(Race.raceid).filter(Race.date <= now).order_by(desc(Race.date)).first()[0]
    results = []
    for x in session.query(Results, Driver).join(Driver, Driver.driverid == Results.driverid).filter(Results.raceid == race).order_by(Results.position):
        results.append({'Position':x.Results.position, 'Driver': x.Driver.forename + ' ' + x.Driver.surname, 'Starting Position': x.Results.grid})
    standings = []
    for y in session.query(Driver_Standings, Driver).join(Driver, Driver.driverid == Driver_Standings.driverid).filter(Driver_Standings.raceid == race).order_by(Driver_Standings.position):
        standings.append({'Position':y.Driver_Standings.position, 'Driver': y.Driver.forename + ' ' + y.Driver.surname, 'Points': y.Driver_Standings.points})
    constructors = []
    for z in session.query(Constructor_Standings, Constructor).join(Constructor, Constructor.constructorid == Constructor_Standings.constructorid).filter(Constructor_Standings.raceid == race).order_by(Constructor_Standings.position):
        constructors.append({'Position':z.Constructor_Standings.position ,'Constructor':z.Constructor.name, 'Points':z.Constructor_Standings.points})
    session.close()
    return {'Results':results, 'Standings':standings, 'Constructors':constructors}

def upcoming_race():
    session = get_session()
    race = session.query(Race).filter(Race.date >= datetime.utcnow()).order_by(Race.date).first()
    session.close()
    return{'Year':race.year, 'Race':race.name, 'Round':race.round, 'Date':race.date.strftime('%m-%d-%Y %H:%M:%S')}

def is_lights_out():
    session = get_session()
    race = session.query(Race).filter(Race.date == datetime.utcnow()).order_by(Race.date).first()
    if race == None:
        session.close()
        return {'Race':None, 'status': False}
    if datetime.utcnow().replace(tzinfo=None) >= (race.date - timedelta(minutes=15)):
        session.close()
        return {'Race':race.name, 'status': True}
    session.close()
    return {'Race':race.name, 'status': True}

# Finds the exact status stored in the database
def status_match(status, session):
    return(session.query(Status.statusid).filter(Status.status == status).first())[0]
