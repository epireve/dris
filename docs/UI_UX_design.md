# DRIS UI/UX Design Mockups

This document describes the layout and structure for key templates in the DRIS web application.

### a) Base Template (`base.html`)

The base template provides a consistent structure for all pages in the application.

**Layout & Structure:**

*   **Header:** Contains the NADMA logo on the left and an emergency hotline (999) on the right.
*   **Navigation Bar:** A simple navigation bar with links that change based on user role (e.g., Login/Register, Dashboard, Report Disaster).
*   **Main Content:** A block that will be populated by child templates.
*   **Footer:** A sticky footer containing the copyright notice, your name, and student ID.

**Code Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}DRIS{% endblock %}</title>
    <!-- Link to CSS framework like Bootstrap -->
</head>
<body>
    <header style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #ccc;">
        <div><!-- NADMA Logo Image --> NADMA</div>
        <div>Emergency Hotline: <strong>999</strong></div>
    </header>

    <nav>
        <!-- Navigation links here -->
    </nav>

    <main class="container">
        {% block content %}
        <!-- Page-specific content will go here -->
        {% endblock %}
    </main>

    <footer style="text-align: center; padding: 10px; margin-top: 20px; border-top: 1px solid #ccc;">
        <p>&copy; 2025 NADMA, [Your Full Name], [Your Student ID]</p>
    </footer>
</body>
</html>
```

### b) Other Templates

#### Template for Viewing and Filtering Disaster Reports

*   **Purpose:** To allow all users (especially Authorities) to view a list of all submitted disaster reports and filter them to find relevant information quickly.
*   **Design:**
    *   **Filters:** A form at the top of the page with dropdowns for `Disaster Type` and `Severity`, and a text input for `Location`. A "Filter" button applies the search.
    *   **Report List:** The reports are displayed in a table or as a series of cards. Each entry shows key information: Type, Location (GPS), Severity, Status, and Timestamp.
    *   **Actions:** For Authority users, each report will have a "Details" button to view more information and manage assignments.

#### Template for Submitting Aid Requests OR Registering as a Volunteer

*   **Purpose:** To provide a simple form for a specific user action.
*   **Design (Aid Request Form for Citizens):**
    *   A clean, single-column form.
    *   **Fields:**
        *   Dropdown for `Aid Type` (Food, Shelter, Rescue, Medical).
        *   A `textarea` for `Description` to provide more details.
        *   A `Submit Request` button.
    *   The form will be pre-filled with the user's identity on the backend.
*   **Design (Volunteer Registration/Profile Form for Volunteers):**
    *   A form to capture or update volunteer-specific information.
    *   **Fields:**
        *   A `textarea` or tag-input field for `Skills` (e.g., "First Aid, Driving, Communication").
        *   A checkbox for `Availability` ("I am currently available to help").
        *   An `Update Profile` button.

---

# DRIS UI/UX Design

## Overview

The Disaster Response Information System (DRIS) is designed for three main user roles:
- **Citizen**: Report disasters, request aid, view their own reports/requests.
- **Volunteer**: View/respond to aid requests, manage their volunteer profile.
- **Authority/Admin**: Manage disaster reports, aid requests, volunteers, shelters, and view analytics.

The UI is built with Bootstrap for a modern, responsive, and accessible experience.

---

## Base Template

- **Navbar**: Dynamic links based on user role (Home, Manage Reports, Manage Aid, Manage Shelters, Analytics, Login/Logout, Register).
- **Hero Section**: Full-width welcome and role-based intro.
- **Quick Actions**: Cards for key actions (e.g., Report Disaster, Request Aid, Manage Shelters).
- **Footer**: Credits and copyright.

---

## Key Pages

### Home
- Role-based quick actions and navigation.
- Welcome hero.

### Disaster Reports
- List, filter, and detail views.
- Submit report (citizen).
- Manage/verify (authority/admin).

### Aid Requests
- List, filter, and detail views.
- Submit request (citizen).
- Assign/respond (volunteer, authority).

### Volunteer Registration/Profile
- Registration form.
- Profile management.

### Authority Analytics
- Dashboard cards and charts for disaster, aid, assignment stats.

### Shelter Directory
- Public list with location, capacity, availability.
- Filtering by location and availability.
- Add/edit (authority/admin).

### Authentication
- Login, registration, logout.

---

## UI/UX Principles

- **Consistency**: Bootstrap components, color scheme, and spacing.
- **Accessibility**: ARIA labels, proper form labels, keyboard navigation.
- **Responsiveness**: Mobile-friendly layouts.
- **Feedback**: Success/error messages, alerts, and badges.

---

## Example Wireframe (Text)

```
+-------------------------------------------------------------+
| Navbar: [Home] [Manage Reports] [Manage Aid] [Shelters] ... |
+-------------------------------------------------------------+
| Hero: Welcome to DRIS                                       |
| [Role-based intro]                                          |
+-------------------------------------------------------------+
| Quick Actions:                                              |
| [Report Disaster] [Request Aid] [Manage Shelters] ...       |
+-------------------------------------------------------------+
| Main Content (List, Form, Dashboard, etc.)                  |
+-------------------------------------------------------------+
| Footer: By Firdaus Adib (23096377) DRIS 2025.               |
+-------------------------------------------------------------+
```

---

## Color Palette

- Primary: #3498db (blue)
- Secondary: #2c3e50 (dark blue)
- Success: #28a745 (green)
- Danger: #dc3545 (red)
- Info: #17a2b8 (teal)
- Light: #f8f9fa
- Dark: #343a40

---

## Typography

- Headings: Bold, clear, Bootstrap defaults.
- Body: Readable, sufficient contrast.

---

## Accessibility

- All forms have labels.
- Buttons and badges have ARIA labels.
- Alerts use `role="alert"`.
- Sufficient color contrast.

---

## Next Steps

See [Navigation_Flow.md](Navigation_Flow.md) for user journeys and navigation diagrams.