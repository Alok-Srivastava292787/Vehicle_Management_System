# 🚚 Freight Fleet Lifecycle Management System - Full Production Document

---

# 1. Project Proposal Document

## 1.1 Executive Summary
The freight company operates 200+ vehicles and faces operational inefficiencies due to manual processes, lack of real-time monitoring, and inconsistent data handling. 

This project proposes a fully automated system leveraging:
- Python-based microservices
- PostgreSQL (OLTP + analytics)
- Kafka (streaming)
- dbt (transformations)
- Airflow (orchestration)
- Streamlit (dashboarding)

---

## 1.2 Problem Statement
- Manual tracking of vehicle movement
- No reliable load or operational metrics
- Inefficient maintenance lifecycle
- Poor inventory tracking in workshops
- Data inconsistencies across systems
- Heavy reliance on Excel

---

## 1.3 Goals
- Real-time vehicle tracking
- Daily operational cost calculation
- Maintenance automation & alerts
- Inventory accuracy
- Elimination of manual errors

---

## 1.4 Architecture

GPS → FastAPI → Kafka → Python Consumer → PostgreSQL → dbt → Streamlit

---

# 2. PostgreSQL Schema (Production)

## 2.1 Schemas
```sql
CREATE SCHEMA master;
CREATE SCHEMA reference;
CREATE SCHEMA transaction;
CREATE SCHEMA timeseries;
```

---

## 2.2 Reference Tables
```sql
CREATE TABLE reference.vehicle_type_ref (
    vehicle_type_id SERIAL PRIMARY KEY,
    vehicle_type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE reference.maintenance_type_ref (
    maintenance_type_id SERIAL PRIMARY KEY,
    maintenance_type_name VARCHAR(50)
);
```

---

## 2.3 Master Tables
```sql
CREATE TABLE master.vehicle_master (
    vehicle_rc_id VARCHAR(20) PRIMARY KEY,
    vehicle_type_id INT REFERENCES reference.vehicle_type_ref(vehicle_type_id),
    gps_id VARCHAR(50),
    fuel_type VARCHAR(20),
    fuel_capacity NUMERIC,
    last_pm_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 2.4 Time-series Table
```sql
CREATE TABLE timeseries.gps_raw_data (
    id BIGSERIAL PRIMARY KEY,
    vehicle_rc_id VARCHAR(20),
    gps_timestamp TIMESTAMP,
    latitude NUMERIC,
    longitude NUMERIC,
    speed NUMERIC
);
```

---

# 3. ETL Pipeline Implementation

## 3.1 Architecture
Simulator → FastAPI → Kafka → Consumer → Transform → PostgreSQL

---

## 3.2 FastAPI Ingestion
```python
from fastapi import FastAPI
from kafka import KafkaProducer
import json

app = FastAPI()
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post('/ingest')
def ingest(data: dict):
    producer.send('gps_data', value=data)
    return {'status': 'sent'}
```

---

## 3.3 Kafka Consumer
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'gps_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for msg in consumer:
    print(msg.value)
```

---

## 3.4 Transformation Example
```python
def clean(data):
    if data['speed'] < 0:
        return None
    return data
```

---

## 3.5 PostgreSQL Loader
```python
import psycopg2

conn = psycopg2.connect(dbname='fleet_db', user='postgres', password='pass')
```

---

# 4. Streamlit Dashboard (Starter)
```python
import streamlit as st

st.title('Fleet Dashboard')
st.metric('Active Vehicles', 25)
```

---

# 5. POC Success Criteria
- GPS ingest latency < 5 sec
- Data correctness validated
- Dashboard visibility achieved

---

# 6. Deployment Steps
1. Setup PostgreSQL
2. Setup Kafka
3. Run FastAPI
4. Run consumer
5. Launch Streamlit

---

# ✅ End of Production Document
