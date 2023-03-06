# Helper functions and main functions for updating the database using data from ERGAST (ses ergast.py)
from datetime import datetime
from models import Race, Constructor, Constructor_Results, Driver, Driver_Standings
from models import Results, Status, Constructor_Standings
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import ergast

# Function for creating the session object to connect to the PostgreSQL Database
def get_session():
    engine = sqlalchemy.create_engine("postgresql://noah-howren:v2_3wcKR_YFyh6PzHaAE6d4Px2YqngLM@db.bit.io/noah-howren/f1_db")
    Session = sessionmaker(bind = engine)
    return Session()

# Converts constructor reference to constructor identificatin
def con_to_id(con, session):
    return(session.query(Constructor.constructorid).filter(Constructor.constructorref == con).first())[0]

# Converts driver reference to driver identification
def ref_to_id(ref, session):
    return(session.query(Driver).filter(Driver.driverref == ref).first())

# Finds the exact status stored in the database
def status_match(status, session):
    return(session.query(Status.statusid).filter(Status.status == status).first())[0]

# Returns the next race
def next_race():
    session = get_session()
    r = session.query(Race).filter(Race.date >= datetime.utcnow()).order_by(Race.date).first()
    session.close()
    return r

# Checks ERGAST drivers for a given year and inserts any that is not already in the table
def update_drivers(year, session):
    res = ergast.cache_drivers(year)['MRData']['DriverTable']['Drivers']
    for x in res:
        if session.query(Driver).filter(Driver.driverref == x['driverId']).first() ==  None:
            d = Driver(driverref = x['driverId'], number = x['permanentNumber'], 
                       code = x['code'], forename = x['givenName'], 
                       surname = x['familyName'], dob = x['dateOfBirth'], 
                       nationality = x['nationality'], url = x['url'])
            session.add(d)
    session.commit()

# Checks ERGAST constructor results for a given race and calculates and inserts values into table 
def update_c_results(race):
    session = get_session()
    try:
        res = ergast.cache_con_res(race)['MRData']['ConstructorTable']['Constructors']
    except:
        return False
    for r in res:
        c_id = con_to_id(r['constructorId'], session)
        p = session.query(Results.points).filter(Results.raceid == race.raceid, Results.constructorid == c_id).all()
        re = Constructor_Results(raceid = race.raceid, constructorid = c_id, points = p[0][0] + p[1][0])
        session.add(re)
    session.commit()
    session.close()
    return True

# Updates driver and results tables
# Returns false if the API doesn't have the data
# Returns true if all the data is received
def update_results(race):
    try:
        res = ergast.cache_results(race)['MRData']['RaceTable']['Races'][0]['Results']
    except:
        return False
    session = get_session()
    # Check to see if driver list has been updated
    update_drivers(race.year, session)
    for r in res:
        d = ref_to_id(r['Driver']['driverId'], session)
        c_i = con_to_id(r['Constructor']['constructorId'], session) 
        real = Results(
            raceid = race.raceid,
            driverid = d.driverid,
            number = d.number,
            constructorid = c_i,
            position = r['position'],
            positiontext = r['positionText'],
            positionorder = r['position'],
            points = r['points'],
            grid = r['grid'],
            laps = r['laps'],
            statusid = status_match(r['status'], session)
        )
        try:
            real.fastestlap = r['FastestLap']['lap']
            real.rank = r['FastestLap']['rank']
            real.fastestlapspeed = r['FastestLap']['AverageSpeed']['speed']
            real.fastestlaptime = r['FastestLap']['Time']['time']
            real.time = r['Time']['time']
            real.milliseconds = r['Time']['millis']
        except:
            pass
        session.add(real)
    session.commit()
    session.close()
    return True

# Updates driver standings table, returning false if it fails
def update_standings(race):
    session = get_session()
    try:
        res = ergast.cache_standings(race.year)['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    except:
        return False
    update_drivers(race.year, session)
    for r in res:
        real = Driver_Standings(
            raceid = race.raceid,
            driverid = ref_to_id(r['Driver']['driverId'], session).driverid,
            points = r['points'],
            wins = r['wins'],
            position = r['position'],
            positiontext = r['positionText'])
        session.add(real)
    session.commit()
    session.close()
    return True

# Updates constructor standings table, returning false if it fails.
def update_c_standings(race):
    session = get_session()
    try:
        res = ergast.cache_c_standings(race.year)['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    except:
        return False
    for r in res:
        print(r)
        real = Constructor_Standings(raceid = race.raceid,
                                      constructorid= con_to_id(r['Constructor']['constructorId'], session),
                                      points = r['points'],
                                      position = r['position'],
                                      positiontext = r['positionText'],
                                      wins = r['wins'])
        session.add(real)
    session.commit()
    session.close()
    return True