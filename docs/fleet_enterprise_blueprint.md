# 🚀 Freight Fleet Lifecycle Management - Enterprise Production Blueprint

---

# 1. Overview
This document extends the production system with:
- dbt (Bronze → Silver → Gold transformations)
- Airflow (orchestration)
- Alerting system (real-time + batch)

---

# 2. dbt Data Transformation Layer

## 2.1 Bronze Layer (Raw Data)

```sql
-- models/bronze/gps_raw.sql
SELECT * FROM timeseries.gps_raw_data;
```

## 2.2 Silver Layer (Cleaned Data)

```sql
-- models/silver/gps_clean.sql
SELECT
    vehicle_rc_id,
    gps_timestamp,
    latitude,
    longitude,
    speed
FROM {{ ref('gps_raw') }}
WHERE latitude BETWEEN -90 AND 90
  AND longitude BETWEEN -180 AND 180
  AND speed >= 0;
```

## 2.3 Gold Layer (Analytics)

```sql
-- models/gold/vehicle_daily_distance.sql
SELECT
    vehicle_rc_id,
    DATE(gps_timestamp) AS trip_date,
    COUNT(*) * 0.5 AS approx_distance_km
FROM {{ ref('gps_clean') }}
GROUP BY vehicle_rc_id, DATE(gps_timestamp);
```

---

# 3. Airflow Orchestration

## 3.1 DAG Example

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'fleet_etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@hourly',
    catchup=False
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /dbt && dbt run'
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /dbt && dbt test'
    )

    dbt_run >> dbt_test
```

---

# 4. Alerting Framework

## 4.1 Real-Time Alerts (Streaming)

Implemented inside Kafka Consumer:

```python
if data['speed'] > 100:
    send_alert('Overspeed detected', data)
```

## 4.2 Predictive Alerts

- Maintenance due based on mileage
- Fuel anomaly detection
- Idle vehicle alerts

## 4.3 Batch Alerts (Airflow)

```python
if daily_distance > threshold:
    trigger_alert('High usage vehicle')
```

---

# 5. Alert Delivery Channels

- Email
- SMS
- xMatters / Webhooks
- Dashboard notifications

---

# 6. Monitoring & Observability

- Prometheus (metrics)
- Grafana (dashboards)
- Logging (ELK stack)

---

# 7. End-to-End Flow

GPS → FastAPI → Kafka → Consumer → PostgreSQL → dbt → Airflow → Alerts → Streamlit

---

# ✅ End of Enterprise Blueprint
