# Freight Fleet Management System - Artifacts

## 1. Project Proposal Document

### Executive Summary
The freight company is currently facing operational inefficiencies due to reliance on manual processes, inconsistent data, and lack of real-time visibility. This project proposes implementation of an automated system using Python, PostgreSQL, Kafka, and Streamlit.

### Problem Statement
- No automated vehicle tracking despite GPS
- Lack of load and cost data
- Inefficient maintenance
- Poor inventory management
- Manual data errors

### Proposed Solution
- Real-time GPS monitoring
- Maintenance lifecycle tracking
- Inventory management
- Cost analytics
- Alerting system

### Architecture
GPS → FastAPI → Kafka → Python Consumer → PostgreSQL → dbt → Streamlit Dashboard

---

## 2. PostgreSQL Schema (Initial DDL)

### Schemas
CREATE SCHEMA master;
CREATE SCHEMA reference;
CREATE SCHEMA transaction;
CREATE SCHEMA timeseries;

### Sample Tables

CREATE TABLE master.vehicle_master (
    vehicle_rc_id VARCHAR(20) PRIMARY KEY,
    vehicle_type_id INT,
    gps_id VARCHAR(50),
    fuel_type VARCHAR(20)
);

CREATE TABLE timeseries.gps_raw_data (
    id BIGSERIAL PRIMARY KEY,
    vehicle_rc_id VARCHAR(20),
    gps_timestamp TIMESTAMP,
    latitude NUMERIC,
    longitude NUMERIC,
    speed NUMERIC
);

---

## 3. ETL PIPELINE IMPLEMENTATION

### Components
- FastAPI ingestion service
- Kafka streaming
- Python consumer
- PostgreSQL loader

### Sample API Code

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

### Pipeline Flow
Simulator → API → Kafka → Consumer → Transform → PostgreSQL

---

## End of Document
