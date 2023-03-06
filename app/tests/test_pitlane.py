import json

# Was to establish baseline for testing
def test_home(client):
    response = client.get("/")
    assert response.json['message'] == 'Welcome to the Pitlane 🏎️'

def test_createleague(client):
    data = {
        "userid": "ByaetFWO0aPHIIdW7gI3QqrioHF2",
        "leagueName": "Unit Testing League"
    }
    response = client.post("/fantasy/createLeague",
                            data=json.dumps(data),
                            headers={"Content-Type": "application/json"})
    # assert (response.json['status'] == '200') and (response.json['inviteCode'])
    if len(response.json['inviteCode']) == 5:
        data2 = {
            "teamInformation": {
                "teamname": "Unit Testing Team",
                "userid": "ByaetFWO0aPHIIdW7gI3QqrioHF2",
                "roster": {
                    "d1": "Alexander Albon",
                    "d2": "Fernando Alonso",
                    "d3": "Valtteri Bottas",
                    "d4": "Nyck de Vries",
                    "d5": "Pierre Gasly"
                },
                "constructorid": "Ferrari",
                "inviteCode": response.json['inviteCode'],
                "notificationFlag": True,
            }
        }
        response2 = client.post("/fantasy/createTeam",
                                data=json.dumps(data2),
                                headers={"Content-Type": "application/json"})
        assert response2.json['success'] is True

def test_team(client):
    data = {
        "userid": "ByaetFWO0aPHIIdW7gI3QqrioHF2"
    }
    response = client.post("/fantasy",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"})
    # the [0][0] is because i want the first team and just the team name which i know
    assert response.json['teams'][0][0] == "Unit Testing Team"
