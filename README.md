# DRIS (Disaster Response Information System)

A minimal Django-based system for disaster response coordination.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install django
```

3. Configure the project:
- Ensure core app is added to INSTALLED_APPS in settings.py
- Set AUTH_USER_MODEL = 'core.User' in settings.py
- Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run development server:
```bash
python manage.py runserver
```

## Features

1. Custom User Model with role-based access (Citizen, Volunteer, Authority)
2. Disaster Report management
3. Aid Request handling
4. Shelter management

## Project Structure

- `core/` - Main application
  - `models.py` - Database models
  - `forms.py` - Forms for user registration
  - `views.py` - Views for authentication
  - `templates/` - HTML templates

## Documentation

- Data Model: [docs/Data_model.md](docs/Data_model.md)
