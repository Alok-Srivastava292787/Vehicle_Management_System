# TEST_CATALOG.md

# Vehicle Management System - Test Catalog

## Purpose

This document tracks automated API test coverage implemented in the project.

---

# Vehicle Module

```text
Create Vehicle
Get Vehicle
Get All Vehicles
Update Vehicle
Deactivate Vehicle
Not Found
```

Status:

```text
PASSED
```

---

# Driver Module

```text
Create Driver
Get Driver
Get All Drivers
Update Driver
Deactivate Driver
Not Found
```

Status:

```text
PASSED
```

---

# Employee Module

```text
Create Employee
Get Employee
Get All Employees
Update Employee
Deactivate Employee
Not Found
```

Status:

```text
PASSED
```

---

# Part Module

```text
Create Part
Get Part
Get All Parts
Update Part
Deactivate Part
Not Found
```

Status:

```text
PASSED
```

---

# Complaint Module

```text
Create Complaint
Get Complaint
Get All Complaints
Update Complaint
Deactivate Complaint
Not Found
```

Status:

```text
PASSED
```

---

# Inspection Module

```text
Create Inspection
Get Inspection
Get All Inspections
Update Inspection
Deactivate Inspection
Not Found
```

Status:

```text
PASSED
```

---

# Job Card Module

```text
Create Job Card
Get Job Card
Get All Job Cards
Update Job Card
Deactivate Job Card
Get Job Card Not Found
Update Job Card Not Found
Deactivate Job Card Not Found
```

Status:

```text
PASSED
```

---

# Job Card Parts Module

```text
Create Job Card Part
Get Job Card Part
Get All Job Card Parts
Update Job Card Part
Deactivate Job Card Part
Not Found
```

Status:

```text
PASSED
```

---

# Part Requisition Module

Implemented Tests:

```text
test_create_requisition

test_get_requisition

test_get_all_requisitions

test_update_requisition

test_delete_requisition

test_get_requisition_not_found

test_update_requisition_not_found

test_delete_requisition_not_found
```

Status:

```text
PASSED
```

---

# Part Requisition Detail Module

Implemented Tests:

```text
test_create_requisition_detail

test_get_requisition_detail

test_get_all_requisition_details

test_update_requisition_detail

test_delete_requisition_detail

test_get_requisition_detail_not_found

test_update_requisition_detail_not_found

test_delete_requisition_detail_not_found
```

Status:

```text
PASSED
```

---

# PDF Validation Tests

## Job Card PDF

Validated:

```text
PDF Opens
Vehicle Details Present
Parts Displayed
Cost Summary Displayed
Footer Displayed
```

Status:

```text
PASSED
```

---

## Part Requisition PDF

Validated:

```text
PDF Opens
Part Names Displayed
Qty Required Displayed
Qty Returned Displayed
Signature Section Displayed
Footer Displayed
```

Status:

```text
PASSED
```

---

# Integration Test Coverage

```text
Complaint → Inspection

Inspection → Job Card

Job Card → Job Card Parts

Job Card → Requisition

Requisition → Requisition Detail

Requisition → PDF

Job Card → PDF
```

Status:

```text
PASSED
```

---

# Release Candidate Test Result

Version:

```text
v1.0.0-RC1
```

Result:

```text
PASS
```

Ready For:

```text
Demo
UAT
Sprint 2 Planning
```