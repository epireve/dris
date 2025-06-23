# DRIS (Disaster Response Information System)

## Overview

DRIS is a Django-based web application for disaster reporting, aid coordination, volunteer management, and shelter directory, supporting real-time updates via Django Channels.

---

## Setup & Installation

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
4. **Seed initial data (optional)**
   ```bash
   python manage.py populate_data
   ```
5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

---

## Running the Server

### For Real-Time Features (ASGI/Channels)

> **Important:** To enable real-time updates (WebSockets), you must run the server with Daphne (ASGI server):

```bash
daphne DRIS_Project.asgi:application
```

- By default, this runs on port 8000. To specify a port:
  ```bash
  daphne -p 8000 DRIS_Project.asgi:application
  ```

### For Standard Django (No Real-Time)

If you do not need real-time features, you can use the standard Django runserver:

```bash
python manage.py runserver
```

---

## Features

- Disaster reporting and management
- Aid request and assignment
- Volunteer registration and coordination
- Shelter directory with filtering and management
- Real-time updates for disaster reports and shelter availability (via WebSockets)
- Role-based navigation and permissions
- Responsive, accessible Bootstrap UI

---

## Real-Time Updates

- WebSocket endpoint: `/ws/updates/`
- Real-time updates are broadcast to all connected clients when disaster reports or shelters are updated.

---

## Documentation

- UI/UX Design: `docs/UI_UX_design.md`
- Navigation Flow: `docs/Navigation_Flow.md`
- Data Model: `docs/Data_model.md`

---

## Credits

By Firdaus Adib (23096377)

DRIS 2025.
