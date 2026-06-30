from config import ALERT_SPEED_THRESHOLD

def send_alert(message, data):
    print(f"🚨 ALERT: {message} | Data: {data}")

def check_alerts(data):
    # Overspeed alert
    if data["speed"] > ALERT_SPEED_THRESHOLD:
        send_alert("Overspeed detected", data)

    # Idle alert
    if data["speed"] == 0:
        send_alert("Vehicle idle", data)
# maintenance alert
def maintenance_alert(data):
    if data["total_maintenance_cost"] > 50000:
        send_alert("High maintenance cost", data)

    if data.get("downtime_hours", 0) > 24:
        send_alert("High vehicle downtime", data)

# Extend Alert System (Fuel + Salary)
def fuel_alert(data):
    if data["total_fuel_cost"] > 10000:
        send_alert("High fuel expense", data)

def salary_alert(data):
    if data["net_salary"] < 0:
        send_alert("Invalid salary", data)
