import json

def test_home(client):
    response = client.get("/")
    assert response.json['message'] == 'Welcome to the Pitlane 🏎️'

def test_team(client):
    data = {
        "userid": "ByaetFWO0aPHIIdW7gI3QqrioHF2"
    }
    response = client.post("/fantasy",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"})
    assert response.json['teams'] == [["Test Team", 7]]