# Script for updating database, created by Noah Howren, implementing code developed by Anthony Ganci and Colin Martires

import db
from datetime import datetime
import time
import logging
import notifications

def get_info():
    return {'currentTime':datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S"), 'nextRace':race.name, 'nextRaceDateTime':race.date.strftime("%m/%d/%Y, %H:%M:%S")}

if __name__ == "__main__":
    logging.basicConfig(filename='pitlane.log', level=logging.INFO)
    logging.info({'pitlaneScript':datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S") })
    # Saves the race that is coming up next
    x = True

    while(x == True):
        race = db.next_race()
        desired_date = race.date - datetime.timedelta(days = 3)
        desired_date = desired_date.replace(hour = 12, minute = 0)
        diff         = desired_date - datetime.now()

        while(datetime.now() != desired_date):
            logging.info(get_info())
            if diff > 7200:
                time.sleep(7200)
                diff = diff - 7200
            else:
                logging.info(get_info())
                time.sleep(diff)
        
        logging.info(notifications.upcomingRaceNotifs())

        desired_date = race.date - datetime.timedelta(minute = 15)
        diff         = desired_date - datetime.utcnow()
        while(datetime.utcnow() != desired_date):
            logging.info(get_info())
            if diff > 7200:
                time.sleep(7200)
                diff = diff - 7200
            else:
                time.sleep(diff)
        
        logging.info(notifications.lightsOutNotifs())

        time.sleep(7200)

        logging.info(get_info())

        # Results aren't posted right away so if the race results aren't in yet, wait for 10 minutes and check again, repeat for all of the update functions
        r_f = False
        while (r_f == False):
            r_f = db.update_results()
            time.sleep(600)
        c_f = False
        while(c_f == False):
            c_f = db.update_c_results()
            time.sleep(600)
        s_f = False
        while(s_f == False):
            s_f = db.update_standings()
            time.sleep(600)
        f_f = False
        while(f_f == False):
            f_f = db.update_c_standings()
            time.sleep(600)

        logging.info(notifications.postRaceNotifs())
        db.score()