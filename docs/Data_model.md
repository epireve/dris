# DRIS Data Model Design

This document outlines the minimal data model for the DRIS prototype application.

### Entity Relationship Summary

* **User:** A custom User model with a `role` field to distinguish between Citizens, Volunteers, and Authorities.
* **DisasterReport:** A citizen can create disaster reports with location and severity.
* **AidRequest:** A citizen can make aid requests linked to disaster reports.
* **Shelter:** A standalone entity for managing available shelter resources.

### Tables (Models)

#### 1. User
*(Extends Django's AbstractUser)*

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `username` | `CharField` | Unique, for login |
| `password` | `CharField` | Hashed by Django |
| `role` | `CharField` | Choices: 'CITIZEN', 'VOLUNTEER', 'AUTHORITY' |

#### 2. DisasterReport

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `reporter` | `ForeignKey(User)` | The citizen who reported it |
| `disaster_type` | `CharField` | Choices: 'Flood', 'Landslide', 'Haze', 'Other' |
| `latitude` | `DecimalField` | GPS coordinate |
| `longitude` | `DecimalField` | GPS coordinate |
| `severity` | `CharField` | Choices: 'Low', 'Medium', 'High' |
| `timestamp` | `DateTimeField` | Auto-generated on creation |

#### 3. AidRequest

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `requester` | `ForeignKey(User)` | The citizen requesting aid |
| `disaster_report` | `ForeignKey(DisasterReport)` | Optional link to a disaster report |
| `aid_type` | `CharField` | Choices: 'Food', 'Shelter', 'Rescue' |
| `status` | `CharField` | Choices: 'Pending', 'Fulfilled' |

#### 4. Shelter

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `location` | `CharField` | Address or description |
| `capacity` | `IntegerField` | Maximum number of people |
| `availability` | `IntegerField` | Current available spots |

### Relationships

* User (1) --- (M) DisasterReport: A user can create multiple disaster reports
* User (1) --- (M) AidRequest: A user can make multiple aid requests
* DisasterReport (1) --- (M) AidRequest: A disaster report can have multiple aid requests
* Shelter is standalone, referenced in AidRequest if needed