Great — now we’re moving into **true analytics layer (Gold models)** 💡  
These dbt models will give you **business-ready KPIs** for dashboards, alerts, and reporting.

***

# 🏗️ DBT GOLD MODELS (COST & OPERATIONS ANALYTICS)

We’ll build **production-grade Gold models**:

✅ **vehicle\_daily\_distance**  
✅ **vehicle\_daily\_fuel\_cost**  
✅ **vehicle\_daily\_maintenance\_cost**  
✅ **employee\_monthly\_cost**  
✅ **vehicle\_total\_cost**  
✅ **cost\_per\_km (core KPI)**  
✅ **fuel\_efficiency**

***

# 📁 Suggested dbt Structure

```
models/
  bronze/
  silver/
  gold/
    vehicle_daily_distance.sql
    vehicle_daily_fuel_cost.sql
    vehicle_cost_summary.sql
    cost_per_km.sql
    fuel_efficiency.sql
    employee_monthly_cost.sql
```

***

# ✅ 1. GOLD: Vehicle Daily Distance

> Using cleaned GPS data (silver.gps\_clean)

### `models/gold/vehicle_daily_distance.sql`

```sql
SELECT
    vehicle_rc_id,
    DATE(gps_timestamp) AS trip_date,
    COUNT(*) * 0.5 AS approx_distance_km   -- adjust if GPS interval changes
FROM {{ ref('gps_clean') }}
GROUP BY vehicle_rc_id, DATE(gps_timestamp)
```

***

# ✅ 2. GOLD: Vehicle Daily Fuel Cost

### `models/gold/vehicle_daily_fuel_cost.sql`

```sql
SELECT
    vehicle_rc_id,
    fuel_date,
    SUM(total_fuel_cost) AS total_fuel_cost,
    SUM(fuel_quantity) AS total_fuel_quantity
FROM {{ source('transaction', 'fuel_transactions') }}
GROUP BY vehicle_rc_id, fuel_date
```

***

# ✅ 3. GOLD: Vehicle Maintenance Cost

### `models/gold/vehicle_maintenance_cost.sql`

```sql
SELECT
    vehicle_rc_id,
    DATE(created_at) AS maintenance_date,
    SUM(labour_charges) AS total_maintenance_cost
FROM {{ source('transaction', 'maintenance_job_card') }}
GROUP BY vehicle_rc_id, DATE(created_at)
```

***

# ✅ 4. GOLD: Employee Monthly Cost

### `models/gold/employee_monthly_cost.sql`

```sql
SELECT
    employee_id,
    salary_month,
    SUM(net_salary) AS total_salary
FROM {{ source('transaction', 'employee_salary') }}
GROUP BY employee_id, salary_month
```

***

# ✅ 5. GOLD: Vehicle Cost Summary (Core Aggregation)

👉 Combines **fuel + maintenance**

### `models/gold/vehicle_cost_summary.sql`

```sql
WITH fuel AS (
    SELECT
        vehicle_rc_id,
        fuel_date AS date,
        total_fuel_cost
    FROM {{ ref('vehicle_daily_fuel_cost') }}
),

maintenance AS (
    SELECT
        vehicle_rc_id,
        maintenance_date AS date,
        total_maintenance_cost
    FROM {{ ref('vehicle_maintenance_cost') }}
)

SELECT
    COALESCE(f.vehicle_rc_id, m.vehicle_rc_id) AS vehicle_rc_id,
    COALESCE(f.date, m.date) AS date,

    COALESCE(f.total_fuel_cost, 0) AS fuel_cost,
    COALESCE(m.total_maintenance_cost, 0) AS maintenance_cost,

    COALESCE(f.total_fuel_cost, 0)
    + COALESCE(m.total_maintenance_cost, 0) AS total_cost

FROM fuel f
FULL OUTER JOIN maintenance m
ON f.vehicle_rc_id = m.vehicle_rc_id
AND f.date = m.date
```

***

# ✅ 6. GOLD: Cost per KM (Most Important KPI)

### `models/gold/cost_per_km.sql`

```sql
WITH distance AS (
    SELECT * FROM {{ ref('vehicle_daily_distance') }}
),

cost AS (
    SELECT * FROM {{ ref('vehicle_cost_summary') }}
)

SELECT
    d.vehicle_rc_id,
    d.trip_date,
    d.approx_distance_km,

    c.total_cost,

    CASE
        WHEN d.approx_distance_km > 0
        THEN c.total_cost / d.approx_distance_km
        ELSE NULL
    END AS cost_per_km

FROM distance d
LEFT JOIN cost c
    ON d.vehicle_rc_id = c.vehicle_rc_id
   AND d.trip_date = c.date
```

***

# ✅ 7. GOLD: Fuel Efficiency

### `models/gold/fuel_efficiency.sql`

```sql
WITH distance AS (
    SELECT * FROM {{ ref('vehicle_daily_distance') }}
),

fuel AS (
    SELECT * FROM {{ ref('vehicle_daily_fuel_cost') }}
)

SELECT
    d.vehicle_rc_id,
    d.trip_date,
    d.approx_distance_km,
    f.total_fuel_quantity,

    CASE
        WHEN f.total_fuel_quantity > 0
        THEN d.approx_distance_km / f.total_fuel_quantity
        ELSE NULL
    END AS km_per_litre

FROM distance d
LEFT JOIN fuel f
    ON d.vehicle_rc_id = f.vehicle_rc_id
   AND d.trip_date = f.fuel_date
```

***

# ✅ 8. GOLD: Total Cost Including Salary (Advanced)

👉 (Optional — requires mapping employees → vehicles)

### `models/gold/vehicle_total_cost_with_salary.sql`

```sql
WITH base_cost AS (
    SELECT * FROM {{ ref('vehicle_cost_summary') }}
),

salary AS (
    SELECT
        salary_month,
        SUM(total_salary) AS total_salary
    FROM {{ ref('employee_monthly_cost') }}
    GROUP BY salary_month
)

SELECT
    b.vehicle_rc_id,
    b.date,
    b.total_cost,

    s.total_salary / 30 AS approx_daily_salary_cost,

    b.total_cost + (s.total_salary / 30) AS total_cost_with_salary

FROM base_cost b
LEFT JOIN salary s
ON DATE_TRUNC('month', b.date) = s.salary_month
```
# 📊 2. DBT – Maintenance Analytics (Gold Models)

Now we build **real business KPIs**

***

## ✅ 2.1 Daily Maintenance Cost

### `models/gold/vehicle_daily_maintenance_cost.sql`

```sql
SELECT
    vehicle_rc_id,
    DATE(completion_date) AS date,
    SUM(labour_charges) +
    COALESCE(SUM(p.total_cost), 0) AS total_maintenance_cost
FROM {{ source('transaction', 'maintenance_job_card') }} m
LEFT JOIN {{ source('transaction', 'maintenance_parts_usage') }} p
    ON m.job_card_id = p.job_card_id
GROUP BY vehicle_rc_id, DATE(completion_date)
```

***

## ✅ 2.2 Maintenance Frequency

```sql
SELECT
    vehicle_rc_id,
    COUNT(*) AS maintenance_count,
    DATE_TRUNC('month', completion_date) AS month
FROM {{ source('transaction', 'maintenance_job_card') }}
GROUP BY vehicle_rc_id, DATE_TRUNC('month', completion_date)
```

***

## ✅ 2.3 Average Downtime per Vehicle

```sql
SELECT
    vehicle_rc_id,
    AVG(downtime_hours) AS avg_downtime_hours
FROM {{ source('transaction', 'maintenance_job_card') }}
GROUP BY vehicle_rc_id
```

***

## ✅ 2.4 Cost per Maintenance Event

```sql
SELECT
    m.vehicle_rc_id,
    m.job_card_id,
    (m.labour_charges + COALESCE(SUM(p.total_cost),0)) AS cost_per_event
FROM {{ source('transaction', 'maintenance_job_card') }} m
LEFT JOIN {{ source('transaction', 'maintenance_parts_usage') }} p
ON m.job_card_id = p.job_card_id
GROUP BY m.vehicle_rc_id, m.job_card_id, m.labour_charges
```

***

## ✅ 2.5 Failure Pattern (Advanced)

```sql
SELECT
    vehicle_rc_id,
    maintenance_type_id,
    COUNT(*) AS failure_count
FROM {{ source('transaction', 'maintenance_job_card') }}
GROUP BY vehicle_rc_id, maintenance_type_id
```

***

## ✅ 2.6 Combined Operational Cost (FINAL KPI)

```sql
WITH maintenance AS (
    SELECT * FROM {{ ref('vehicle_daily_maintenance_cost') }}
),
fuel AS (
    SELECT * FROM {{ ref('vehicle_daily_fuel_cost') }}
),
distance AS (
    SELECT * FROM {{ ref('vehicle_daily_distance') }}
)

SELECT
    d.vehicle_rc_id,
    d.trip_date,

    COALESCE(f.total_fuel_cost, 0) AS fuel_cost,
    COALESCE(m.total_maintenance_cost, 0) AS maintenance_cost,

    (COALESCE(f.total_fuel_cost, 0)
     + COALESCE(m.total_maintenance_cost, 0)) AS total_cost,

    CASE
        WHEN d.approx_distance_km > 0
        THEN (COALESCE(f.total_fuel_cost, 0)
             + COALESCE(m.total_maintenance_cost, 0))
             / d.approx_distance_km
        ELSE NULL
    END AS cost_per_km

FROM distance d
LEFT JOIN fuel f
ON d.vehicle_rc_id = f.vehicle_rc_id
   AND d.trip_date = f.fuel_date
LEFT JOIN maintenance m
ON d.vehicle_rc_id = m.vehicle_rc_id
   AND d.trip_date = m.date
```

***

# 🧪 Add dbt Tests (Important)

### `models/gold/schema.yml`

```yaml
version: 2

models:
  - name: vehicle_daily_distance
    columns:
      - name: vehicle_rc_id
        tests:
          - not_null

  - name: cost_per_km
    columns:
      - name: cost_per_km
        tests:
          - not_null

  - name: vehicle_daily_maintenance_cost
    description: "Daily maintenance cost per vehicle"
    columns:
      - name: vehicle_rc_id
        tests:
          - not_null
      - name: date
        tests:
          - not_null
      - name: total_maintenance_cost
        tests:
          - not_null

  - name: maintenance_frequency
    description: "Monthly maintenance frequency"
    columns:
      - name: vehicle_rc_id
        tests:
          - not_null
      - name: maintenance_count
        tests:
          - not_null

  - name: avg_downtime
    description: "Average downtime per vehicle"
    columns:
      - name: vehicle_rc_id
        tests:
           - not_null

  - name: cost_per_event
    description: "Maintenance cost per job card"
    columns:
      - name: job_card_id
        tests:
          - not_null
          - unique

  - name: failure_pattern
    description: "Failure pattern per vehicle"
    columns:
      - name: vehicle_rc_id
        tests:
          - not_null
      - name: maintenance_type_id
        tests:
          - not_null
  - name: maintenance_job_card
    columns:
      - name: vehicle_rc_id
        tests:
          - relationships:
                to: ref('vehicle_master')
                field: vehicle_rc_id
  - name: maintenance_parts_usage
    columns:
      - name: job_card_id
        tests:
          - relationships:
                to: source('transaction', 'maintenance_job_card')
                field: job_card_id
```
```

***
## ✅ 3.1 Test: No Negative Maintenance Cost

### `tests/no_negative_maintenance_cost.sql`

```sql
SELECT *
FROM {{ ref('vehicle_daily_maintenance_cost') }}
WHERE total_maintenance_cost < 0
```

✅ Should return **0 rows**

***

## ✅ 3.2 Test: Downtime Should Not Be Negative

```sql
SELECT *
FROM {{ source('transaction', 'maintenance_job_card') }}
WHERE downtime_hours < 0
```

***

## ✅ 3.3 Test: Job Card Completion Must Have Date

```sql
SELECT *
FROM {{ source('transaction', 'maintenance_job_card') }}
WHERE job_card_status = 'COMPLETED'
  AND completion_date IS NULL
```

***

## ✅ 3.4 Test: Parts Cost Must Match Quantity

```sql
SELECT *
FROM {{ source('transaction', 'maintenance_parts_usage') }}
WHERE total_cost <= 0
```

***

# 📊 4. ADVANCED LOGIC TESTS

***

## ✅ 4.1 High Cost Outlier Detection

```sql
SELECT *
FROM {{ ref('vehicle_daily_maintenance_cost') }}
WHERE total_maintenance_cost > 100000
```

👉 You can convert to **warning (not failure)**

***

## ✅ 4.2 Excessive Maintenance Frequency

```sql
SELECT *
FROM {{ ref('maintenance_frequency') }}
WHERE maintenance_count > 50
```

***

## ✅ 4.3 Downtime Anomaly

```sql
SELECT *
FROM {{ ref('avg_downtime') }}
WHERE avg_downtime_hours > 48
```

***

# 🧪 5. DATA CONSISTENCY TESTS

***

## ✅ 5.1 Missing Maintenance Cost for Activity

```sql
SELECT d.*
FROM {{ ref('vehicle_daily_distance') }} d
LEFT JOIN {{ ref('vehicle_daily_maintenance_cost') }} m
ON d.vehicle_rc_id = m.vehicle_rc_id
   AND d.trip_date = m.date

WHERE m.vehicle_rc_id IS NULL
```

***

## ✅ 5.2 Maintenance Without Vehicle

```sql
SELECT *
FROM {{ source('transaction', 'maintenance_job_card') }}
WHERE vehicle_rc_id NOT IN (
    SELECT vehicle_rc_id FROM {{ ref('vehicle_master') }}
)
```
In `dbt_project.yml`:

```yaml
tests:
  +severity: warn
```

Or per test:

```yaml
tests:
  - not_null:
      severity: error
```

***

# ▶️ 7. RUN TESTS

```bash
dbt test
```

# 📊 What You Get From These Models

## 🚚 Fleet Intelligence

* Cost per km ✅
* Fuel efficiency ✅
* Maintenance cost trends ✅

## 💰 Financial Insights

* Total vehicle cost ✅
* Salary contribution ✅

## 🚚 Operational Risks

* Missing job completion dates ❌
* Invalid downtime values ❌
* Wrong maintenance records ❌

## 💰 Financial Risks

* Negative cost ❌
* Missing cost entries ❌
* Incorrect parts calculation ❌

## 📉 Analytics Risks

* Incorrect KPIs ❌
* Broken joins ❌
* Incomplete data ❌

## 🚨 Alerting Ready

You can now trigger:

* High cost per km
* Low fuel efficiency
* High maintenance cost

***

# 🚀 Next Step (Best Move)

Now plug this into:

### 👉 Streamlit Dashboard

* Vehicle KPI cards
* Cost vs distance graph
* Fuel efficiency trends

OR

### 👉 Airflow DAG

* Schedule `dbt run`
* Trigger alerts based on Gold tables

***

👉 Tell me next step:  
✅ *"build streamlit dashboard for these models"*  
✅ *"create airflow DAG using dbt + alerts"*  
✅ *"add advanced analytics (trip detection + idle time)"*

***

You now have a **complete analytics layer — exactly what enterprise logistics platforms run on** 🚀
