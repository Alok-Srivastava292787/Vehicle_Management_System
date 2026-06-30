from datetime import datetime
import math

def process_gps_data(data):
    try:
        lat, lon = data["latitude"], data["longitude"]

        # Validation
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return None

        # Timestamp conversion
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])

        # Derived fields
        data["is_moving"] = data["speed"] > 5

        return data

    except Exception as e:
        print("Transform error:", e)
        return None

# Fuel Transform Logic
def process_fuel_data(data):
    try:
        # Calculate cost if missing
        if not data.get("total_fuel_cost"):
            data["total_fuel_cost"] = (
                data["fuel_quantity"] * data["fuel_price_per_unit"]
            )

        # Simple validation
        if data["fuel_quantity"] <= 0:
            return None

        return data

    except Exception as e:
        print("Fuel transform error:", e)
        return None
# salary_transform logic
def calculate_salary(base, allowances, deductions):
    return base + allowances - deductions

# maintenance_transform logic
def process_maintenance(data):
    try:
        # Default cost calculation
        parts_cost = sum(
            p["quantity"] * p.get("price", 0)
            for p in data.get("parts", [])
        )

        data["total_maintenance_cost"] = (
            data.get("labour_charges", 0) + parts_cost
        )

        return data

    except Exception as e:
        print("Maintenance transform error:", e)
        return None