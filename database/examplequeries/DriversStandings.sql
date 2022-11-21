SELECT driver_standings.position, drivers.surname, driver_standings.points
FROM driver_standings
INNER JOIN drivers ON drivers.driverId = driver_standings.driverId
WHERE raceId IN (SELECT raceId 
                FROM races
                WHERE date <= CURRENT_DATE
                ORDER BY date DESC LIMIT 1)
ORDER BY POSITION;