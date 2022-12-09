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
import json
import psycopg2
import pandas as pd


app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
@app.route("/", methods=['GET'])
def index():
    
    return ('Hello! Welcome to the Pitlane 🏎️')
@app.route("/pitlane", methods=['GET', 'POST'])
def pitlane():
    fastf1.Cache.enable_cache('cache/')
    if request.method == 'POST':
        post_data = request.get_json()
        print(request.get_json())
        if post_data['method'] == 'headtohead':
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

            driver1 = race.laps.pick_driver(DATA['driver1'])
            driver2 = race.laps.pick_driver(DATA['driver2'])

            fig, ax = plt.subplots()
            ax.plot(driver1['LapNumber'], driver1['LapTime'], color='red')
            ax.plot(driver2['LapNumber'], driver2['LapTime'], color='cyan')
            ax.set_title(f"{DATA['driver1']} vs {DATA['driver2']}")
            ax.set_xlabel("Lap Number")
            ax.set_ylabel("Lap Time")
            
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return jsonify({'src': pngImageB64String, 'status': 'success'})
        if post_data['method'] == 'gearshift':
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
            tel = lap.get_telemetry()

            x = np.array(tel['X'].values)
            y = np.array(tel['Y'].values)

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            gear = tel['nGear'].to_numpy().astype(float)

            fig = plt.figure()
            cmap = cm.get_cmap('Paired')
            lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
            lc_comp.set_array(gear)
            lc_comp.set_linewidth(4)

            plt.gca().add_collection(lc_comp)
            plt.axis('equal')
            plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

            title = plt.suptitle(
                f"Fastest Lap Gear Shift Visualization\n"
                f"{lap['Driver']} - {session.event['EventName']} {session.event.year}"
            )

            cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
            cbar.set_ticks(np.arange(1.5, 9.5))
            cbar.set_ticklabels(np.arange(1, 9))

            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return jsonify({'src': pngImageB64String, 'status': 'success'})
        if post_data['method'] == 'speedvisual':
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
            colormap = mpl.cm.plasma
            x = lap.telemetry['X']              # values for x-axis
            y = lap.telemetry['Y']              # values for y-axis
            color = lap.telemetry['Speed']      # value to base color gradient on

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
            fig.suptitle(f"{DATA['track']} {DATA['year']} - {DATA['driver']} - Speed", size=24, y=0.97)

            # Adjust margins and turn of axis
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
            ax.axis('off')


            # After this, we plot the data itself.
            # Create background track line
            ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

            # Create a continuous norm to map from data points to colors
            norm = plt.Normalize(color.min(), color.max())
            lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

            # Set the values used for colormapping
            lc.set_array(color)

            # Merge all line segments together
            line = ax.add_collection(lc)


            # Finally, we create a color bar as a legend.
            cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
            normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
            legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return jsonify({'src': pngImageB64String, 'status': 'success'})

    if request.method == 'GET':    
        # return jsonify({'msg': "Welcome to Pitlane 🏎️! Enter information to get started!", 'status': 'success'})
        return jsonify({'status': 'success'})

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
    jsondmp = json.dumps(cursor.fetchall()) 
    conn.close
    return(jsondmp)


def dbconnect():
    conn = psycopg2.connect("postgresql://noah-howren:v2_3wcKR_YFyh6PzHaAE6d4Px2YqngLM@db.bit.io/noah-howren/f1_db")
    conn.autocommit = True
    return (conn)

if __name__ == '__main__':
    app.run(debug=True)