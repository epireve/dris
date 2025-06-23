# DRIS Minimal Data Model (ERD)

## Entities

- **User**
  - id (PK)
  - username
  - password
  - role (Citizen, Volunteer, Authority)

- **DisasterReport**
  - id (PK)
  - user_id (FK to User)
  - type
  - gps_lat
  - gps_long
  - severity
  - timestamp

- **AidRequest**
  - id (PK)
  - user_id (FK to User)
  - disaster_report_id (FK to DisasterReport, optional)
  - type (food, shelter, rescue)
  - status

- **Volunteer**
  - id (PK)
  - user_id (FK to User)
  - skills
  - availability

- **Shelter**
  - id (PK)
  - location
  - capacity
  - availability

## Relationships

- User (1) --- (M) DisasterReport
- User (1) --- (M) AidRequest
- User (1) --- (1) Volunteer
- DisasterReport (1) --- (M) AidRequest
- Shelter is standalone, referenced in AidRequest if needed

## Simple ERD (text)

User --< DisasterReport
User --< AidRequest
User -- Volunteer
DisasterReport --< AidRequest