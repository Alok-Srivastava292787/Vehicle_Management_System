# BUSINESS_RULES.md

# Vehicle Management System - Business Rules

## Purpose

This document captures the functional and business rules implemented within the Vehicle Management System.

---

# 1. Vehicle Management

## Rule BR-001

Every Complaint, Inspection, Job Card and Requisition must be associated with a valid Vehicle.

## Rule BR-002

Vehicles may be marked inactive using:

```text
active_flag = false
```

Inactive vehicles remain available for audit and reporting purposes.

---

# 2. Driver Management

## Rule BR-003

Drivers can be assigned to Job Cards.

## Rule BR-004

Inactive drivers cannot be assigned to newly created records.

---

# 3. Employee Management

## Rule BR-005

Employees may participate in:

```text
Inspection
Job Card Processing
Verification
Approval
Requisition Processing
```

## Rule BR-006

Technician assignment is optional but strongly recommended for maintenance tracking.

---

# 4. Complaint Management

## Rule BR-007

A complaint must belong to a vehicle.

## Rule BR-008

A complaint may result in an inspection.

## Rule BR-009

A complaint may be referenced by one or more job cards.

---

# 5. Inspection Management

## Rule BR-010

Inspection records must reference a vehicle.

## Rule BR-011

Inspections may originate from complaints.

## Rule BR-012

Inspection findings may be used during Job Card creation.

---

# 6. Job Card Management

## Rule BR-013

A Job Card must reference:

```text
Vehicle
Complaint
Inspection
```

## Rule BR-014

Job Card statuses:

```text
OPEN
IN_PROGRESS
WAITING_PARTS
COMPLETED
CANCELLED
```

## Rule BR-015

A Job Card is the primary maintenance execution document.

## Rule BR-016

Multiple parts may be linked to a Job Card.

---

# 7. Job Card Parts

## Rule BR-017

A Job Card may contain multiple part records.

Relationship:

```text
1 Job Card
N Parts
```

## Rule BR-018

Parts usage tracks:

```text
Part
Quantity
Unit Price
Total Cost
```

## Rule BR-019

Total Parts Cost is calculated as:

```text
Quantity × Unit Price
```

---

# 8. Part Requisition

## Rule BR-020

A Part Requisition must reference:

```text
Vehicle
Job Card
```

## Rule BR-021

A requisition may optionally reference a technician.

## Rule BR-022

Requisition Number is system generated.

Format:

```text
PR-YYYY-NNNNNN

Example:

PR-2026-000043
```

## Rule BR-023

Allowed requisition statuses:

```text
OPEN
APPROVED
ISSUED
CLOSED
```

## Rule BR-024

One Job Card may create multiple requisitions.

Relationship:

```text
1 Job Card
N Requisitions
```

---

# 9. Part Requisition Detail

## Rule BR-025

Each Requisition Detail must belong to a Requisition.

Relationship:

```text
1 Requisition
N Detail Lines
```

## Rule BR-026

Each detail line references one Part.

## Rule BR-027

Requisition Detail tracks:

```text
Part
Qty Required
Qty Returned
Required Serial Number
Returned Serial Number
Remarks
```

## Rule BR-028

Quantity Returned cannot exceed Quantity Required.

(Recommended Validation Rule)

---

# 10. PDF Generation

## Rule BR-029

Job Cards can be downloaded as PDF.

## Rule BR-030

Part Requisitions can be downloaded as PDF.

## Rule BR-031

PDFs must contain:

```text
Header Information
Details
Approvals
Footer
```

---

# 11. Audit Rules

## Rule BR-032

Audit logs are generated for:

```text
INSERT
UPDATE
```

operations.

## Rule BR-033

Audit records are retained permanently.

## Rule BR-034

Audit records are not editable by end users.

---

# 12. Soft Delete Rules

## Rule BR-035

Records are not physically deleted.

Instead:

```text
active_flag = false
```

is applied.

## Rule BR-036

Inactive records remain available for:

```text
Audit
History
PDF Generation
Reporting
```

---

# 13. Dashboard Rules

## Rule BR-037

Dashboard metrics are calculated using active transactional data.

## Rule BR-038

Recent Activity displays latest operations from audit tracking.

---

# 14. Future Planned Rules

## Inventory Management

```text
Part Issue
Part Return
Stock Tracking
```

## Approvals

```text
Store Approval
Maintenance Approval
Manager Approval
```