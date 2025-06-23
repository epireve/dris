# DRIS System Report

## Overview

The Disaster Response Information System (DRIS) is a web-based platform designed to streamline disaster reporting, aid requests, volunteer coordination, and authority management. The system supports three main user roles: Citizen, Volunteer, and Authority/Admin.

---

## Problem Statement

Malaysia faces frequent natural disasters such as floods, landslides, and haze. Current disaster management methods are fragmented, causing delays in reporting, aid delivery, and volunteer coordination. NADMA requires a centralized system to improve coordination and communication for disaster response.

## Proposed Solution

DRIS is a centralized, web-based platform built with Django. It serves as a single point of contact for citizens, volunteers, and authorities, providing real-time updates on disaster reports and shelter availability. The system is designed to be secure, modular, and user-friendly.

---

## Goals & Objectives

- Streamline disaster event reporting by citizens.
- Efficiently manage and fulfill aid requests.
- Coordinate volunteers based on skills and availability.
- Provide a centralized, up-to-date directory of emergency shelters.
- Empower authorities with a dashboard for monitoring and managing all response activities.

---

## User Personas

- **Citizen:** Members of the public affected by or witnessing a disaster. They report incidents and request aid (food, shelter, rescue).
- **Volunteer:** Individuals who want to help. They register their skills and availability and receive assignments from authorities.
- **Authority:** NADMA staff or authorized personnel. They monitor the situation, manage resources, coordinate shelters, and assign volunteers to tasks.

---

## Key Features

- **Emergency Hotline Banner:** Prominently displays the emergency hotline (999) at the top of every page.
- **Role-Based Navigation:** Dynamic navigation and dashboard content based on user role.
- **Disaster Reporting:** Citizens can submit disaster reports with geolocation via a searchable, draggable map pin.
- **Aid Requests:** Citizens can request aid linked to disaster reports; authorities and volunteers can manage and respond.
- **Shelter Directory:** Public and managed directory of shelters, including location, capacity, and availability.
- **Volunteer Management:** Volunteers can register, update profiles, and be assigned to aid tasks.
- **Analytics Dashboard:** Authorities can view statistics and manage all aspects of disaster response.
- **Responsive UI:** Built with Bootstrap for accessibility and mobile-friendliness.
- **Real-time Updates:** Disaster reports and shelter availability are updated in real time for all users.

---

## Functional Requirements

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| User Management          | Role-based registration and login for Citizens, Volunteers, and Authorities |
| Disaster Reporting       | Citizens report disaster events with type, GPS, severity, and timestamp     |
| Aid Request Management   | Citizens submit aid requests (food, shelter, rescue)                        |
| Volunteer Coordination   | Volunteers register skills/availability; authorities assign tasks           |
| Shelter Directory        | Public list of shelters with location, capacity, and availability           |
| Administrative Dashboard | Authorities manage users, reports, shelters, and assignments                |

---

## Non-Functional Requirements

| Requirement    | Description                                                         |
|----------------|---------------------------------------------------------------------|
| Architecture   | Follows Django's Model-View-Template (MVT) architecture             |
| Security       | Secure authentication and role-based access control (RBAC)          |
| Code Quality   | Modular, maintainable, and reusable codebase                        |
| Real-time      | Real-time updates for disaster reports and shelter availability     |

---

## Technical Stack

- **Framework:** Django
- **Frontend:** Django templates, Bootstrap, Leaflet.js for maps
- **Database:** SQLite3 (for prototype)
- **Architecture:** Model-View-Template (MVT)
- **Admin:** Django-admin for backend management

---

## Documentation

- [Data Model](Data_model.md): Entity relationships and database schema.
- [Navigation Flow](Navigation_Flow.md): User journeys, navigation diagrams, and access matrix.
- [UI/UX Design](UI_UX_design.md): Template structure, wireframes, and design principles.

---

## Recent Enhancements

- Emergency hotline banner with marquee effect.
- NADMA logo and blended background image in the hero section.
- Disaster report submission with map search and draggable pin, integrated in the form card.

---

## System Structure

- **Backend:** Django (Python)
- **Frontend:** Django templates, Bootstrap, Leaflet.js for maps
- **Static Assets:** Located in `staticfiles/`
- **Documentation:** All docs in [`docs/`](docs/)

---

## Key Deliverables

- **Data Model:** See [`docs/Data_model.md`](Data_model.md:1) for schema and relationships.
- **UI/UX Design:** See [`docs/UI_UX_design.md`](UI_UX_design.md:1) for mockups and layout.
- **Navigation Flow:** See [`docs/Navigation_Flow.md`](Navigation_Flow.md:1) for user journeys and diagrams.
- **Final Implementation:** Django project `DRIS_Project` with all specified requirements.

---

## System Screenshots

### Registration and Profile

**Registration Page**
![Registration](../images/dris_registration.png)
The registration page allows new users to create an account by providing essential details. The process is streamlined to ensure quick access for citizens, volunteers, and authorities.

**Role Selection During Registration**
![Role Selection](../images/dris_registration_selecting_role.png)
During registration, users select their intended role (Citizen, Volunteer, Authority), which tailors their experience and access within the system.

**Profile Dropdown**
![Profile Dropdown](../images/profile_dropdown_view.png)
The profile dropdown menu provides users with quick access to their account settings and logout functionality, ensuring secure and convenient session management.

---

### Authority/Admin Views

**Homepage for Authority**
![Authority Homepage](../images/authority_01_homepage.png)
The authority dashboard serves as the central hub for disaster management, providing real-time updates and direct access to disaster reports, aid requests, shelters, and analytics.

**Disaster Report List and Detail**
![Disaster Reports List](../images/authority_02_disaster_reports.png)
Authorities can view and filter all submitted disaster reports. Each report entry includes disaster type, location, severity, and status, with interactive map previews for spatial context.

![Disaster Report Detail](../images/authority_02_disaster_report_view.png)
Detailed view of a specific disaster report. Authorities can inspect the report's information, view the precise location on an interactive map, and take management actions as needed.

**Aid Requests List and Detail**
![Aid Requests List](../images/authority_03_aid_requests.png)
Authorities can monitor, filter, and process all incoming aid requests, ensuring timely and effective disaster response.

![Aid Request Detail](../images/authority_03_aid_request_view.png)
Each aid request detail page provides comprehensive information, including requester, type of aid, and status, with options to assign volunteers or update fulfillment status.

**Shelter Directory and Management**
![Shelter Directory](../images/authority_04_shelter_directory.png)
A comprehensive directory of available shelters, displaying location, capacity, and current availability. Authorities can quickly assess and manage shelter resources.

![Shelter Edit](../images/authority_04_shelter_edit.png)
Authorities can edit shelter details, update capacity, and manage availability to ensure optimal resource allocation during disasters.

![Shelter Edit Filter](../images/authority_04_shelter_edit_filter.png)
The shelter directory supports advanced filtering, allowing authorities to efficiently locate and manage shelters based on specific criteria.

**Analytics Dashboard**
![Analytics Dashboard](../images/authority_05_analytics.png)
The analytics dashboard provides visual insights into disaster trends, aid requests, and resource allocation, supporting data-driven decision-making for authorities.

---

### Citizen Views

**Disaster Reports List and Detail**
![Citizen Disaster Reports](../images/citizen_02_disaster_reports.png)
Citizens can view a list of their submitted disaster reports, each with status indicators and interactive map previews for easy tracking and spatial awareness.

![Citizen Disaster Report Detail](../images/citizen_02_disaster_report_view.png)
Each disaster report detail page features an interactive map, allowing citizens to review the exact location of the reported incident and all associated details.

**Submit Disaster Report**
![Submit Disaster Report](../images/citizen_02_submit_disaster_report.png)
The disaster report submission form enables citizens to report incidents efficiently. The form includes fields for disaster type, severity, and description.

![Interactive Map for Disaster Report](../images/citizen_02_submit_disaster_report_interactive_map.png)
During disaster reporting, citizens can search for a location and precisely place a pin on the interactive map by dragging and dropping, ensuring accurate geolocation of the incident.

**Aid Requests**
![Submit Aid Request](../images/citizen_03_aid_request_submit.png)
Citizens can submit aid requests specifying the type of assistance needed. The process is integrated with disaster reports for seamless support.

![View Aid Request](../images/citizen_03_aid_request_view.png)
Citizens can view the status and details of their submitted aid requests, including fulfillment progress and any authority or volunteer responses.

---

### Volunteer Views

**Volunteer Homepage**
![Volunteer Homepage](../images/volunteer_01_homepage.png)
The volunteer dashboard provides an overview of assigned tasks and quick access to disaster and aid management features.

**Disaster Reports and Aid Requests**
![Volunteer Disaster Reports](../images/volunteer_02_disaster_reports.png)
Volunteers can view disaster reports relevant to their assignments, with interactive map integration for situational awareness.

![Volunteer Aid Requests](../images/volunteer_03_aid_requests.png)
A list of aid requests available for volunteers to respond to, with filtering and sorting options for efficient task management.

![Aid Request Take Action](../images/volunteer_03_aid_request_view_take_action.png)
Volunteers can view detailed information about aid requests and take direct action, such as accepting assignments or updating status.