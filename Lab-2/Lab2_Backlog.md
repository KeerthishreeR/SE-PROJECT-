# Lab 2: Agile Backlog and Sprint Plan - Pharmacy Expiry & Re-order Engine

Four Epics and ten User Stories worth 34 story points, split into two
one-week sprints. Priorities use Jira's levels; points use the Fibonacci scale.

## Epics

| Epic | Description | Stories | Points |
| --- | --- | --- | --- |
| Epic 1: FEFO Stock Allocation | Record every delivered batch and always dispense from the valid batch that expires first. | 1.1 to 1.3 | 13 |
| Epic 2: Expiry Monitoring and Alerts | Warn staff about batches nearing expiry early enough to act on them. | 2.1 to 2.2 | 5 |
| Epic 3: Re-order and Supplier Dispatch | Turn low stock into purchase orders that suppliers can see once they are dispatched. | 3.1 to 3.3 | 10 |
| Epic 4: Inventory Visibility and Performance | Give staff a clear view of stock and give managers proof that the system performs. | 4.1 to 4.2 | 6 |

## User Stories

| Summary | Description | Priority | Points | Sprint |
| --- | --- | --- | --- | --- |
| Story 1.1: Record delivered batches | As a pharmacy technician, I want to register each delivery with its batch number, expiry date and quantity, so that every pack on the shelf can be traced. | High | 3 | 1 |
| Story 1.2: Allocate earliest-expiring batch | As a pharmacist, I want the system to pick the valid batch with the earliest expiry date when I dispense, so that older stock leaves the shelf first. | Highest | 5 | 1 |
| Story 1.3: Reject expired batch at checkout | As a cashier, I want an expired batch to be rejected at checkout and the next valid batch suggested, so that I never sell out-of-date medicine. | Highest | 5 | 1 |
| Story 2.1: 30-day expiry warning list | As a pharmacy manager, I want a daily list of batches expiring within 30 days, so that I can return or discount them in time. | High | 3 | 1 |
| Story 2.2: Dashboard expiry alerts | As a pharmacist, I want near-expiry alerts shown on my dashboard when I log in, so that I notice them without running a report. | Medium | 2 | 2 |
| Story 3.1: Set minimum stock per medicine | As a pharmacy manager, I want to set a minimum stock level for each medicine, so that the system knows when to reorder. | High | 2 | 2 |
| Story 3.2: Draft purchase order at low stock | As a pharmacy manager, I want a draft purchase order created when stock falls below its minimum, so that shortages are prevented without manual checks. | High | 5 | 2 |
| Story 3.3: Supplier views dispatched orders | As a supplier, I want to see the purchase orders dispatched to me, so that I can prepare the delivery. | Medium | 3 | 2 |
| Story 4.1: Inventory status screen | As a pharmacy staff member, I want one screen showing the quantity, expiry date and status of every batch, so that I can answer stock questions quickly. | Medium | 3 | 2 |
| Story 4.2: Performance and availability report | As a pharmacy manager, I want a report on response times and uptime, so that I can confirm the system copes with busy hours. | Low | 3 | Backlog |

## Sprint plan

| Sprint | Goal | Stories | Points |
| --- | --- | --- | --- |
| Sprint 1 | Safe FEFO dispensing: record batches, pick the earliest valid one, reject expired stock and warn about near-expiry batches. | 1.1, 1.2, 1.3, 2.1 | 16 |
| Sprint 2 | Close the loop: set re-order levels, draft purchase orders, show suppliers their orders and surface alerts and stock status. | 2.2, 3.1, 3.2, 3.3, 4.1 | 15 |
| Backlog | Left for a later sprint. | 4.2 | 3 |
