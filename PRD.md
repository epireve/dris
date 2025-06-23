# Disaster Response Information System (DRIS) - Product Requirements Document

## 1. Introduction

### 1.1. Problem Statement
In response to the increasing frequency of natural disasters in Malaysia (floods, landslides, haze), the National Disaster Management Agency (NADMA) requires a centralized system to improve coordination and communication. Current methods are fragmented, leading to delays in reporting, aid delivery, and volunteer management.

Stack: Django, Django-admin, Sqlite3, Bootstrap

### 1.2. Proposed Solution
The Disaster Response Information System (DRIS) will be a centralized, web-based platform developed using the Django framework. It will serve as the single point of contact for citizens needing help, volunteers offering assistance, and authorities managing the overall response effort. The system will provide real-time updates on disaster reports and shelter availability.

### 1.3. Goals & Objectives
*   To streamline the reporting of disaster events by citizens.
*   To efficiently manage and fulfill aid requests.
*   To coordinate volunteers based on their skills and availability.
*   To provide a centralized and up-to-date directory of emergency shelters.
*   To empower authorities with a dashboard for monitoring and managing all response activities.

## 2. User Personas

The system will serve three primary user roles:

*   **2.1. Citizen:** A member of the public affected by or witnessing a disaster. Their primary goal is to report incidents and request necessary aid (food, shelter, rescue).
*   **2.2. Volunteer:** An individual who wants to help. Their primary goal is to register their skills and availability and receive assignments from authorities.
*   **2.3. Authority:** A NADMA staff member or authorized personnel. Their primary goal is to monitor the situation, manage resources, coordinate shelters, and assign volunteers to tasks.

## 3. System Requirements

### 3.1. Functional Requirements

| Feature | Description |
| :--- | :--- |
| **User Management** | Allow role-based registration and login for Citizens, Volunteers, and Authorities. |
| **Disaster Reporting** | Enable Citizens to report disaster events including disaster type, GPS coordinates, severity, and timestamp. |
| **Aid Request Management** | Allow Citizens to submit aid requests specifying types of aid such as food, shelter, or rescue. |
| **Volunteer Coordination** | Enable Volunteers to register their skills and availability; allow Authorities to assign them to tasks. |
| **Shelter Directory** | Display a public list of shelters including location, capacity, and availability. |
| **Administrative Dashboard** | Enable Authorities to manage all users, reports, shelters, and assignments. |

### 3.2. Non-Functional Requirements

| Requirement | Description |
| :--- | :--- |
| **Architecture** | The application must follow a Model-View-Controller (MVC) architecture. |
| **Security** | Implement secure authentication and role-based access control (RBAC). |
| **Code Quality** | The codebase must be modular and maintainable, utilizing reusable components. |
| **Real-time Updates** | The system should incorporate real-time updates for disaster reports and shelter availability. |

## 4. Technical Stack

*   **Framework:** Django
*   **Architecture:** Model-View-Template (MVT), which is Django's implementation of MVC.

## 5. Key Deliverables & Documentation

The development process requires the creation of specific design documents before implementation. These documents are detailed in the `/docs` directory.

*   **Data Model:** A detailed breakdown of the database schema, entities, and relationships.
    *   **Task:** Create the `Data_Model.md` file as per the instructions in Question 1.
*   **UI/UX Design:** Mockups and structural descriptions for the application's base template and key pages.
    *   **Task:** Create the `UI_UX_Design.md` file as per the instructions in Question 2.
*   **Navigation Flow:** A diagram illustrating how different user roles navigate through the application.
    *   **Task:** Create the `Navigation_Flow.md` file as per the instructions in Question 3.
*   **Final Implementation:** A Django project named `DRIS_Project` that implements all the specified requirements.