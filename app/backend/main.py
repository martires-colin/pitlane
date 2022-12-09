from flask import Flask, render_template, jsonify
from flask_cors import CORS
import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
import json
import psycopg2
from psycopg2.extras import RealDictCursor 

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
@app.route("/", methods=['GET'])
def index():
    # return render_template('index.html')
    return ('<p>Hello world</p>')
@app.route("/pitlane", methods=['GET'])
def pitlane():
    # return render_template('index.html')
    
    plotting.setup_mpl()
    race = fastf1.get_session(2020, 'Turkish Grand Prix', 'R')
    race.load()

    lec = race.laps.pick_driver('LEC')
    ham = race.laps.pick_driver('HAM')
    fig, ax = plt.subplots()
    ax.plot(lec['LapNumber'], lec['LapTime'], color='red')
    ax.plot(ham['LapNumber'], ham['LapTime'], color='cyan')
    ax.set_title("LEC vs HAM")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return (pngImageB64String)

# Function that returns connection to database
def dbconnect():
    conn = psycopg2.connect(database="F1_DB",
                            user = "postgres", password = "postgres",
                            host="127.0.0.1", port="5432")
    conn.autocommit = True
    return (conn)

# Function that returns json response containing standings
# (I'm not sure if i formatted this right let me know if I screwed so up -NH)
# @app.route("/standings", methods=['GET'])
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
    
if __name__ == '__main__':
    app.run(debug=True)