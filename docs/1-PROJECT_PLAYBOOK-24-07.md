docs/PROJECT_PLAYBOOK.md
docs/BUSINESS_RULES.md
docs/TEST_CATALOG.md
docs/CLIENT_STORY.md
docs/PPT_STORYBOARD.md
# PROJECT_PLAYBOOK.md

# Vehicle Management System - Project Playbook

## Document Information

| Item | Value |
|--------|--------|
| Project | Vehicle Management System |
| Version | 1.0.0-RC1 |
| Backend | FastAPI |
| Frontend | React + Vite |
| Database | PostgreSQL |
| Reporting | ReportLab PDF |
| Prepared By | Fleet Management Team |
| Status | Release Candidate (RC1) |

---

# 1. Project Overview

The Vehicle Management System is a fleet maintenance and workshop management application designed to manage the complete maintenance lifecycle of vehicles.

The solution provides:

- Vehicle Management
- Driver Management
- Employee Management
- Part Inventory Management
- Complaint Management
- Vehicle Inspection Management
- Job Card Management
- Part Requisition Management
- Audit Trail
- Dashboard and Activity Monitoring
- PDF Document Generation

---

# 2. System Architecture

## Frontend

```text
React
Vite
Ant Design
React Router
Axios
DayJS
```

### Responsibilities

- Master Data Screens
- Dashboard
- Search and Filters
- Workflow Screens
- PDF Access
- Reports

---

## Backend

```text
FastAPI
SQLAlchemy
Pydantic
Uvicorn
Pytest
ReportLab
```

### Responsibilities

- REST APIs
- Validation
- Business Rules
- Database Access
- Audit Management
- PDF Generation

---

## Database

```text
PostgreSQL
```

Schemas:

```text
master
inventory
transact
audit
```

---

# 3. Application Modules

## Master Modules

### Vehicle Master

Stores:

```text
Vehicle Number
RC Number
Make
Model
Registration Details
Status
```

---

### Driver Master

Stores:

```text
Driver Name
License Number
Phone
Status
```

---

### Employee Master

Stores:

```text
Employee Name
Employee Code
Designation
Status
```

---

### Part Master

Stores:

```text
Part Name
Part Number
Category
Unit Price
Stock Information
Status
```

---

## Transaction Modules

### Complaint Management

Tracks:

```text
Vehicle Complaints
Reported Issues
Complaint Creation
Complaint Closure
```

---

### Inspection Management

Tracks:

```text
Vehicle Inspection
Observations
Findings
Recommendations
```

---

### Job Card Management

Tracks:

```text
Maintenance Activities
Technicians
Issue Details
Repair Actions
Parts Used
Maintenance Status
```

---

### Job Card Parts

Tracks:

```text
Part Usage
Quantity
Unit Price
Total Cost
```

---

### Part Requisition Management

Tracks:

```text
Part Requests
Job Card Association
Approval Lifecycle
Store Requests
```

---

### Part Requisition Details

Tracks:

```text
Part Requested
Qty Required
Qty Returned
Required Serial Number
Returned Serial Number
Remarks
```

---

# 4. Database Design

## Schemas

### master

Contains:

```text
vehicle_master
driver_master
employee_master
```

---

### inventory

Contains:

```text
part_master
```

---

### transact

Contains:

```text
complaint
inspection
maintenance_job_card
job_card_part
part_requisition
part_requisition_detail
```

---

### audit

Contains:

```text
audit_log
```

---

# 5. Environment Setup

## Prerequisites

Install:

```text
Python 3.14+
NodeJS 22+
PostgreSQL 16+
Git
VS Code
```

---

# 6. Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Recommended Python Packages

```text
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
python-dotenv
pytest
httpx
reportlab
```

Example versions:

```text
fastapi==0.116.*
sqlalchemy==2.0.*
pydantic==2.*
uvicorn==0.35.*
pytest==8.*
reportlab==4.*
psycopg2-binary==2.9.*
```

---

# 7. Frontend Setup

Install packages:

```bash
npm install
```

Start application:

```bash
npm run dev
```

Build:

```bash
npm run build
```

---

## Main Frontend Dependencies

```text
react
react-dom
react-router-dom
axios
antd
dayjs
vite
```

Example versions:

```text
react 19+
antd 5+
axios 1+
vite 7+
dayjs 1+
```

---

# 8. PostgreSQL Setup

Create database:

```sql
CREATE DATABASE vehicle_management;
```

Create schemas:

```sql
CREATE SCHEMA master;
CREATE SCHEMA inventory;
CREATE SCHEMA transact;
CREATE SCHEMA audit;
```

---

# 9. Environment Variables

## Backend .env

```env
DATABASE_URL=postgresql://user:password@localhost:5432/vehicle_management

APP_NAME=Vehicle Management System

APP_ENV=DEV
```

---

## Frontend .env

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

# 10. Backend Startup

Run API:

```bash
uvicorn app.main:app --reload
```

Swagger:

```text
http://localhost:8000/docs
```

Redoc:

```text
http://localhost:8000/redoc
```

---

# 11. Frontend Startup

```bash
npm run dev
```

Vite URL:

```text
http://localhost:5173
```

---

# 12. Reporting

## Supported Reports

### Job Card PDF

Contains:

```text
Vehicle Details
Technicians
Parts Used
Cost Summary
Approvals
Footer
```

---

### Part Requisition PDF

Contains:

```text
Header Details
Requested Parts
Qty Required
Qty Returned
Totals
Approval Section
Footer
```

---

## Reusable Footer Utility

Location:

```text
app/utils/pdf_footer.py
```

Purpose:

```text
Common footer for all PDF documents.
```

---

# 13. Audit Framework

Audit captures:

```text
INSERT
UPDATE
```

Tracks:

```text
Table Name
Record ID
Operation
Old Values
New Values
User
Timestamp
```

---

# 14. Soft Delete Strategy

Records are not physically deleted.

Instead:

```text
active_flag = false
```

is used.

Benefits:

```text
Audit Compliance
Data Recovery
History Retention
```

---

# 15. Testing

Run all tests:

```bash
pytest -v
```

Run module tests:

```bash
pytest app/tests/test_job_card_api.py -v
```

```bash
pytest app/tests/test_part_requisition_api.py -v
```

```bash
pytest app/tests/test_part_requisition_detail_api.py -v
```

---

# 16. Git Workflow

## Feature Development

```bash
git checkout -b feature/new-feature
```

Commit:

```bash
git add .

git commit -m "Feature description"
```

Push:

```bash
git push origin feature/new-feature
```

---

## Merge Process

```text
Feature Branch
       ↓
Develop
       ↓
Main
```

---

# 17. Release Management

Current Release:

```text
v1.0.0-RC1
```

Tag:

```bash
git tag -a v1.0.0-rc1 -m "Vehicle Management System RC1"

git push origin v1.0.0-rc1
```

---

# 18. Completed Features (RC1)

## Backend

```text
Vehicle API
Driver API
Employee API
Part API

Complaint API
Inspection API
Job Card API
Job Card Parts API

Part Requisition API
Part Requisition Detail API

Audit APIs
Dashboard APIs

Job Card PDF
Part Requisition PDF
```

---

## Frontend

```text
Dashboard

Vehicles
Drivers
Employees
Parts

Complaints
Inspections

Job Cards
Job Card Details

Part Requisitions
Part Requisition Details
```

---

# 19. Known Future Roadmap

## Inventory Management

```text
Part Issue Workflow
Part Return Workflow
Stock Ledger
Stock Movement History
```

---

## Notifications

```text
Email Notifications
Approvals
Escalations
Alerts
```

---

## Analytics

```text
Maintenance Trends
Cost Analysis
Part Consumption Analysis
Vehicle Downtime Reports
```

---

# 20. Support Information

Project:

```text
Vehicle Management System
```

Current Milestone:

```text
Release Candidate 1 (RC1)
```

Status:

```text
Stable
Ready for Demo
Ready for UAT
Ready for Sprint 2 Planning
```