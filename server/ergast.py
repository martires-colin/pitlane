import requests

# Queries ERGAST drivers for a year
def cache_drivers(year):
    response = requests.get('http://ergast.com/api/f1/%s/drivers.json'%(year)).json()
    return(response)

# Queries ERGAST constructors results
def cache_con_res(race):
    response = requests.get('http://ergast.com/api/f1/%s/%s/constructors.json'%(race.year, race.round)).json()
    return(response)

# Queries ERGAST drivers results
def cache_results(race):
    response = requests.get('http://ergast.com/api/f1/%s/%s/results.json'%(race.year, race.round)).json()
    return(response)

def cache_standings(year):
    response = requests.get('http://ergast.com/api/f1/%s/driverStandings.json'%(year)).json()
    return(response)

def cache_c_standings(year):
    response = requests.get('http://ergast.com/api/f1/%s/constructorStandings.json'%(year)).json()
    return(response)