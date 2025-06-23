# DRIS Application Navigation Flow

This diagram and description illustrate the user navigation paths for each role (Citizen, Volunteer, Authority) within the DRIS application.

### Navigation Diagram

```mermaid
graph TD
    A[Homepage / Login] -->|Login as Citizen| B(Citizen Dashboard)
    A -->|Login as Volunteer| C(Volunteer Dashboard)
    A -->|Login as Authority| D(Authority Dashboard)
    A -->|Register| E(Registration Page)

    subgraph Citizen Flow
        B --> B1[Report a New Disaster]
        B --> B2[Request Aid]
        B --> B3[View My Reports/Requests]
        B --> B4[View Shelter Directory]
    end

    subgraph Volunteer Flow
        C --> C1[Update Profile/Skills]
        C --> C2[View Assigned Tasks]
        C --> B4[View Shelter Directory]
    end

    subgraph Authority Flow
        D --> D1[Manage Disaster Reports]
        D --> D2[Manage Aid Requests]
        D --> D3[Manage Shelters]
        D --> D4[Manage Users]
        D --> D5[Assign Volunteers to Tasks]
    end

    D1 --> D5
```

### Flow Description

1.  **Entry Point:** All users start at the `Homepage`, which provides options to `Login` or `Register`. The registration page will ask for the user's intended role.

2.  **Citizen Flow:**
    *   After logging in, a Citizen lands on their dashboard.
    *   From here, they can navigate to:
        *   A form to **Report a New Disaster**.
        *   A form to **Request Aid**.
        *   A page to view the status of their past **Reports and Requests**.
        *   The public **Shelter Directory**.

3.  **Volunteer Flow:**
    *   After logging in, a Volunteer lands on their dashboard.
    *   Their primary navigation options are:
        *   A page to **Update their Profile**, including skills and availability.
        *   A list of their **Assigned Tasks** from Authorities.
        *   The public **Shelter Directory**.

4.  **Authority Flow:**
    *   After logging in, an Authority is taken to the main **Administrative Dashboard**.
    *   This dashboard is the central hub for all management functions:
        *   **Manage Disaster Reports:** View, filter, and update the status of all reports.
        *   **Manage Aid Requests:** View and track all incoming requests.
        *   **Manage Shelters:** Add, edit, or remove shelters and update their availability.
        *   **Manage Users:** View and manage all user accounts.
        *   **Assign Volunteers:** From the disaster report view, an Authority can assign an available volunteer to a specific task.


## User Roles

- **Citizen**
- **Volunteer**
- **Authority/Admin**

---

## Main Navigation Structure

```
[Home] [Disaster Reports] [Aid Requests] [Shelters] [Analytics] [Login/Register or Profile/Logout]
```
- Navigation links are shown/hidden based on user role and authentication status.

---

## Key Navigation Flows

### 1. Citizen

**Typical Journey:**
1. Home → Report Disaster
2. Home → Request Aid
3. Home → My Reports / My Requests
4. Logout

**Navigation:**
- [Home] → [Report Disaster] → [Submit Disaster Report]
- [Home] → [Request Aid] → [Submit Aid Request]
- [Home] → [My Reports] → [Disaster Report List/Detail]
- [Home] → [My Requests] → [Aid Request List/Detail]

---

### 2. Volunteer

**Typical Journey:**
1. Home → View Aid Requests
2. Home → View Disaster Reports
3. Home → Register/Update Volunteer Profile
4. Logout

**Navigation:**
- [Home] → [Aid Requests] → [Aid Request List/Detail]
- [Home] → [Disaster Reports] → [Disaster Report List/Detail]
- [Home] → [Volunteer Profile] → [Register/Update Profile]

---

### 3. Authority/Admin

**Typical Journey:**
1. Home → Manage Reports
2. Home → Manage Aid
3. Home → Manage Shelters
4. Home → Analytics Dashboard
5. Logout

**Navigation:**
- [Home] → [Manage Reports] → [Disaster Report List/Detail/Assignment]
- [Home] → [Manage Aid] → [Aid Request List/Detail/Assignment]
- [Home] → [Manage Shelters] → [Shelter Directory/Add/Edit]
- [Home] → [Analytics] → [Analytics Dashboard]

---

## Navigation Diagram (Text)

```
+-------------------+
|      Home         |
+-------------------+
   |         |         |         |
   v         v         v         v
[Disaster][Aid Req][Shelters][Analytics]
  |           |         |         |
  v           v         v         v
[Detail]   [Detail]   [Add/Edit][Charts]
```

---

## Page Access Matrix

| Page                | Citizen | Volunteer | Authority/Admin |
|---------------------|:-------:|:---------:|:--------------:|
| Home                |   ✔     |    ✔      |      ✔         |
| Disaster Reports    |   ✔     |    ✔      |      ✔         |
| Aid Requests        |   ✔     |    ✔      |      ✔         |
| Shelters            |   ✔     |    ✔      |      ✔         |
| Analytics           |         |           |      ✔         |
| Volunteer Register  |         |    ✔      |                |
| Manage Shelters     |         |           |      ✔         |
| Assign Tasks        |         |           |      ✔         |

---

## User Journey Examples

### Citizen

- **Report Disaster:** Home → Report Disaster → Fill Form → Submit → See My Reports
- **Request Aid:** Home → Request Aid → Fill Form → Submit → See My Requests

### Volunteer

- **Respond to Aid:** Home → Aid Requests → View Details → Respond/Update Status
- **Register as Volunteer:** Home → Volunteer Profile → Register/Update

### Authority/Admin

- **Assign Task:** Home → Manage Aid → Aid Request Detail → Assign Volunteer
- **View Analytics:** Home → Analytics → Dashboard

---

## Notes

- All navigation is mobile-friendly and accessible.
- Unauthorized users are redirected to login or home as appropriate.
- Navigation adapts dynamically to user role and authentication status.