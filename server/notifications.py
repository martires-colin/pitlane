import twilio_config
from twilio.rest import Client
from firebase_admin import db
import firebase_config
import db


def notif(msg_body, phoneNumber):
    client = Client(twilio_config.account_sid, twilio_config.auth_token)
    message = client.messages.create(
            body=msg_body,
            from_=twilio_config.twilio_number,
            to=phoneNumber)
    return message

def postRaceNotifs():
    try:
        database = firebase_config.get_firestore()
        # Get a reference to the users collection
        users_ref = database.collection('users')
        data = db.get_notif()
        res = f'PITLANE\n\nRace Results for {data["Race"]}\n'
        d_s = "PITLANE\n\nDriver's Championship Standings\n"
        c_s = "PITLANE\n\nConstructor's Championship Standings\n"
        for x in data["Results"]:
            res += f'{str(x["Position"]).ljust(3)} {x["Driver"]}\n'
        for y in data['Standings']:
            d_s += f'{str(y["Position"]).ljust(3)} {y["Driver"].ljust(17)} {int(y["Points"])}pts\n'
        for z in data["Constructors"]:
            c_s += f'{str(z["Position"]).ljust(3)} {z["Constructor"].ljust(12)} {int(z["Points"])}pts\n'
        # Iterate over each user and send message to their number depending on flags they have set.
        for user_doc in users_ref.stream():
            user_data = user_doc.to_dict()
            phoneNumber = user_data.get('phoneNumber')
            if phoneNumber:
                if user_data.get('completeNotif') == True:
                    n = notif(res, phoneNumber)
                if user_data.get('driverStandingsNotif') == True:
                    n = notif(d_s, phoneNumber)
                if user_data.get('constructorStandingsNotif') == True:
                    n = notif(c_s, phoneNumber)
        return {'postRaceNotifs':'SUCCESS!', }
    except Exception as inst:
        return {'postRaceNotifs':'FAILURE!', 'ERROR': inst}
    
def upcomingRaceNotifs():
    try:
        database = firebase_config.get_firestore()
        # Get a reference to the users collection
        users_ref = database.collection('users')
        race = db.upcoming_race()
        msg_body = f"PITLANE\n\nUpcoming Race\n{race['Year']}{race['Name']}\nDate: {race['Date']}\n"
        for user_doc in users_ref.stream():
                user_data = user_doc.to_dict()
                phoneNumber = user_data.get('phoneNumber')
                if phoneNumber:
                    if user_data.get('upcomingRacesNotif') == True:
                        notif(msg_body, phoneNumber)
        return {'postRaceNotifs':'SUCCESS!'}   
    except Exception as inst:
        return {'postRaceNotifs':'FAILURE!', 'ERROR': inst}

def lightsOutNotifs():
    try:
        database = firebase_config.get_firestore()
        # Get a reference to the users collection
        users_ref = database.collection('users')
        race = db.upcoming_race()
        msg_body = f"PITLANE\n\nThe \n{race['Name']} is starting soon!\n"
        for user_doc in users_ref.stream():
                user_data = user_doc.to_dict()
                phoneNumber = user_data.get('phoneNumber')
                if phoneNumber:
                    if user_data.get('lightsOutNotif') == True:
                        notif(msg_body, phoneNumber)
        return {'lightsOutNotifs':'SUCCESS!'}   
    except Exception as inst:
        return {'lightsOutNotifs':'FAILURE!', 'ERROR': inst}