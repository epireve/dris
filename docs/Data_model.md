# DRIS Data Model Design

This document outlines the data model for the DRIS application. The model is designed to support the functional requirements, including user roles, disaster reporting, and resource management.

### Entity Relationship Summary

*   **User:** A custom User model will be used to store common data and a `role` field.
*   **DisasterReport:** A citizen (`User`) can create many reports.
*   **AidRequest:** A citizen (`User`) can make many aid requests. Each request can be linked to a `DisasterReport`.
*   **Shelter:** A standalone entity managed by Authorities.
*   **VolunteerAssignment:** A many-to-many link between a volunteer (`User`) and a `DisasterReport`, managed by an Authority.

### Tables (Models)

#### 1. User
*(Extends Django's AbstractUser or uses a one-to-one Profile model)*

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `username` | `CharField` | Unique, for login |
| `password` | `CharField` | Hashed by Django |
| `email` | `EmailField` | Unique, for communication |
| `full_name`| `CharField` | User's full name |
| `role` | `CharField` | Choices: 'CITIZEN', 'VOLUNTEER', 'AUTHORITY' |
| `skills` | `TextField` | For Volunteers only. Stores comma-separated skills. |
| `is_available`| `BooleanField`| For Volunteers only. Default: False. |

#### 2. DisasterReport

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `reporter` | `ForeignKey(User)` | The citizen who reported it. |
| `disaster_type`| `CharField` | Choices: 'Flood', 'Landslide', 'Haze', 'Other' |
| `latitude` | `DecimalField` | GPS coordinate |
| `longitude`| `DecimalField` | GPS coordinate |
| `severity` | `CharField` | Choices: 'Low', 'Medium', 'High', 'Critical' |
| `timestamp` | `DateTimeField` | Auto-generated on creation. |
| `status` | `CharField` | Choices: 'New', 'In Progress', 'Resolved' |

#### 3. AidRequest

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `requester`| `ForeignKey(User)` | The citizen requesting aid. |
| `aid_type` | `CharField` | Choices: 'Food', 'Shelter', 'Rescue', 'Medical' |
| `description`| `TextField` | Details of the request. |
| `status` | `CharField` | Choices: 'Pending', 'Fulfilled' |
| `timestamp`| `DateTimeField` | Auto-generated on creation. |

#### 4. Shelter

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `name` | `CharField` | Name of the shelter. |
| `location` | `CharField` | Address or description of location. |
| `capacity` | `IntegerField` | Maximum number of people. |
| `availability`| `IntegerField` | Current number of available spots. |

#### 5. VolunteerAssignment

| Field Name | Data Type | Description/Constraints |
| :--- | :--- | :--- |
| `id` | `BigAutoField` | Primary Key |
| `volunteer`| `ForeignKey(User)` | The assigned volunteer. `limit_choices_to={'role': 'VOLUNTEER'}` |
| `report` | `ForeignKey(DisasterReport)` | The disaster report this task is related to. |
| `assigned_by`| `ForeignKey(User)` | The authority who made the assignment. `limit_choices_to={'role': 'AUTHORITY'}` |
| `task_description`| `TextField` | Specific instructions for the volunteer. |
| `status` | `CharField` | Choices: 'Assigned', 'Completed' |
| `timestamp`| `DateTimeField` | Auto-generated on creation. |