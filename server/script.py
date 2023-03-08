# Script for updating database, created by Noah Howren, implementing code developed by Anthony Ganci and Colin Martires

import db
from datetime import datetime
import time
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='pitlane.log', level=logging.INFO)
    logging.info({'pitlaneScript':datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S") })
    # Saves the race that is coming up next
    race = db.next_race()
    # While the race hasn't started, the script is trapped in this loop
    while(race.date > datetime.utcnow()):
        info = {'currentTime':datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S"), 'nextRace':race.name, 'nextRaceDateTime':race.date.strftime("%m/%d/%Y, %H:%M:%S")}
        logging.info(info)
        time.sleep(300)
    # Wait 2 hours after race start time to check for results
    time.sleep(7200)

    # Results aren't posted right away so if the race results aren't in yet, wait for 5 minutes and check again, repeat for all of the update functions
    r_f = False
    while (r_f == False):
        r_f = db.update_results()
        time.sleep(300)
    c_f = False
    while(c_f == False):
        c_f = db.update_c_results()
        time.sleep(300)
    s_f = False
    while(s_f == False):
        s_f = db.update_standings()
        time.sleep(300)
    f_f = False
    while(f_f == False):
        f_f = db.update_c_standings()
        time.sleep(300)
    