import json
import psycopg2
from psycopg2.extras import RealDictCursor 
import pandas as pd
def standings():
    conn = dbconnect()
    cursor = conn.cursor()
    cursor.execute('''SELECT driver_standings.position, drivers.surname, driver_standings.points
                    FROM driver_standings
                    INNER JOIN drivers ON drivers.driverId = driver_standings.driverId
                    WHERE raceId IN (SELECT raceId 
                        FROM races
                        WHERE date <= CURRENT_DATE
                        ORDER BY date DESC LIMIT 1)
                    ORDER BY POSITION;''')
    return(json.dumps(cursor.fetchall()))

def dbconnect():
    conn = psycopg2.connect(database="F1_DB",
                            user = "postgres", password = "postgres",
                            host="127.0.0.1", port="5432")
    conn.autocommit = True
    return (conn)


print(pd.read_json(standings()))