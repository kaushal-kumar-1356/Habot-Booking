# Habot Booking System

A simple Django REST API project for managing bookings between Parents and LSAs.

## Features

* Parent and LSA management
* LSA search by skill
* Create booking
* Start time and end time validation
* Double booking prevention
* Booking list and detail API
* Mock payment system
* Payment webhook
* Automated tests using Pytest

## Technologies Used

* Python
* Django
* Django REST Framework
* SQLite
* Pytest
* Pytest-Django

## How to Run

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Run server

```bash
python manage.py runserver
```

The project will run at:

`http://127.0.0.1:8000/`

## API Endpoints

| Method | Endpoint                    | Description            |
| ------ | --------------------------- | ---------------------- |
| GET    | `/api/v1/lsas/search/`      | Search LSAs by skill   |
| POST   | `/api/v1/bookings/`         | Create booking         |
| GET    | `/api/v1/bookings/list/`    | Get all bookings       |
| GET    | `/api/v1/bookings/<id>/`    | Get booking details    |
| POST   | `/api/v1/payments/`         | Create mock payment    |
| POST   | `/api/v1/payments/webhook/` | Handle payment webhook |

## Automated Testing

Run all automated tests using:

```bash
pytest
```

The tests cover:

* Booking creation
* Double booking prevention
* Invalid time validation
* LSA search
* Payment creation
* Payment webhook
* Parent creation

## Payment Flow

```text
Booking
   ↓
Payment
   ↓
SUCCESS
   ↓
Webhook
   ↓
Booking CONFIRMED
```

## Project Structure

```text
Habot Booking/
│
├── manage.py
├── pytest.ini
│
├── config/
│
└── bookings/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── tests.py
```

## Author

Kaushal Kushwah
