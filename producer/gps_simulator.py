import requests, random, time
from datetime import datetime

URL = "http://localhost:8000/ingest"

vehicles = ["TRUCK_1", "TRUCK_2", "TRUCK_3"]

while True:
    payload = {
        "vehicle_rc_id": random.choice(vehicles),
        "timestamp": datetime.utcnow().isoformat(),
        "latitude": random.uniform(12.8, 13.2),
        "longitude": random.uniform(77.4, 77.8),
        "speed": random.uniform(0, 120)
    }
    requests.post(URL, json=payload)
    time.sleep(1)