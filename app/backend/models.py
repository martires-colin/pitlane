# Models for the different database tables to connect to the PITLANE app
# Noah Howren
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Float, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://noah-howren:v2_3wcKR_YFyh6PzHaAE6d4Px2YqngLM@db.bit.io/noah-howren/f1_db")
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()

class Race(Base):
    __tablename__ = "races"
    raceid = Column(Integer, primary_key = True)
    year = Column(Integer)
    round = Column(Integer)
    circuitid = Column(Integer)
    name = Column(String)
    date = Column(Date)
    time = Column(Time)
    url = Column(String)
    fp1_date = Column(Date)
    fp1_time = Column(Time)
    fp2_date = Column(Date)
    fp2_time = Column(Time)
    fp3_date = Column(Date)
    fp3_time = Column(Time)
    quali_date = Column(Date)
    quali_time = Column(Time)
    sprint_date = Column(Date)
    sprint_time = Column(Time)

class Status(Base):
    __tablename__ = "status"
    statusid = Column(Integer, primary_key = True)
    status = Column(String)

class Driver(Base):
    __tablename__ = "drivers"
    driverid = Column(Integer, primary_key = True)
    driverref = Column(String)
    number = Column(Integer)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    dob = Column(String)
    nationality = Column(String)
    url = Column(String)

class Constructor(Base):
    __tablename__ = "constructors"
    constructorid = Column(Integer, primary_key = True)
    constructorref = Column(String)
    name = Column(String)
    nationality = Column(String)
    url = Column(String)

class Circuits(Base):
    __tablename__ = "circuits"
    circuitid = Column(Integer, primary_key = True)
    circuitref = Column(String)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(String)
    url = Column(String)

class Constructor_Results(Base):
    __tablename__ = "constructor_results"
    constructorid = Column(Integer, ForeignKey(Constructor.constructorid), primary_key = True)
    raceid = Column(Integer, ForeignKey(Race.raceid))
    points = Column(Integer)
    status = Column(String)

class Constructor_Standings(Base):
    __tablename__ = "constructor_standings"
    constructorid = Column(Integer, ForeignKey(Constructor.constructorid), primary_key = True)
    raceid = Column(Integer, ForeignKey(Race.raceid))
    points = Column(Integer)
    position = Column(Integer)
    positiontext = Column(String)
    wins = Column(Integer)

class Driver_Standings(Base):
    __tablename__ = "driver_standings"
    driverstandingsid = Column(Integer, primary_key = True)
    raceid = Column(Integer, ForeignKey(Race.raceid))
    driverid = Column(Integer, ForeignKey(Driver.driverid))
    points = Column(Integer)
    position = Column(Integer)
    positiontext = Column(String)
    wins = Column(Integer)

class Lap_Time(Base):
    __tablename__ = "lap_times"
    raceid = Column(Integer, ForeignKey(Race.raceid))
    driverid = Column(Integer, ForeignKey(Driver.driverid))
    lap = Column(Integer, primary_key = True)
    position = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)

class Pit_Stops(Base):
    __tablename__ = "pit_stops"
    raceid = Column(Integer, ForeignKey(Race.raceid))
    driverid = Column(Integer, ForeignKey(Driver.driverid))
    stop = Column(Integer, primary_key = True)
    lap = Column(Integer)
    duration = Column(String)
    milliseconds = Column(Integer)

class Quali(Base):
    __tablename__ = "qualifying"
    qualifyid = Column(Integer, primary_key = True)
    raceid = Column(Integer, ForeignKey(Race.raceid))
    driverid = Column(Integer, ForeignKey(Driver.driverid))
    constructorid = Column(Integer, ForeignKey(Constructor.constructorid))
    number = Column(Integer)
    position = Column(Integer)
    q1 = Column(String)
    q2 = Column(String)
    q3 = Column(String)

class Results(Base):
    __tablename__ = "results"
    resultid = Column(Integer, primary_key = True)
    raceid = Column(Integer, ForeignKey(Race.raceid))
    driverid = Column(Integer, ForeignKey(Driver.driverid))
    constructorid = Column(Integer, ForeignKey(Constructor.constructorid))
    number = Column(Integer)
    grid = Column(Integer)
    position = Column(Integer)
    positiontext = Column(String)
    positionorder = Column(Integer)
    points = Column(Float)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)
    fastestlap = Column(Integer)
    rank = Column(Integer)
    fastestlaptime = Column(String)
    fastestlapspeed = Column(Float)
    statusid = Column(Float, ForeignKey(Status.statusid))

class Season(Base):
    __tablename__ = "seasons"
    year = Column(Integer, primary_key = True)
    url = Column(String)

class SprintResults(Base):
    __tablename__ = "sprint_results"
    resultsid = Column(Integer, primary_key = True)
    raceid = Column(Integer, ForeignKey(Race.raceid))
    driverid = Column(Integer, ForeignKey(Driver.driverid))
    constructorid = Column(Integer, ForeignKey(Constructor.constructorid))
    number = Column(Integer, ForeignKey(Driver.number))
    grid = Column(Integer)
    position = Column(Integer)
    positiontext = Column(String)
    positionorder = Column(Integer)
    points = Column(Integer)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)
    fastestlap = Column(Integer)
    fastestlaptime = Column(String)
    statusid = Column(Integer, ForeignKey(Status.statusid))

class League(Base):
    __tablename__ = 'leagues'
    leagueid = Column(Integer, primary_key = True) 
    creatorid  = Column(String)
    name = Column(String)
    invitecode = Column(String)
    members = Column(Integer)

class Team(Base):
    __tablename__ = 'teams'
    userid = Column(String, primary_key = True) 
    leagueid = Column(Integer, ForeignKey(League.leagueid))
    driver1id = Column(Integer, ForeignKey(Driver.driverid))
    driver2id = Column(Integer, ForeignKey(Driver.driverid))
    constructorid = Column(Integer, ForeignKey(Constructor.constructorid))
    teamname = Column(String)
    notifcationflag = Column(Boolean)