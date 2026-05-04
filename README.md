# SubTracker — Client Subscription Tracker

A Django web application that allows a business to track clients and their subscription status. Built as a technical assessment project for Codverts Systems Ltd.

---

## Features

- **Client Management** — Add, view, edit, and delete clients
- **Subscription Tracking** — Track start date, expiry, amount paid, and payment status
- **Dashboard** — Overview of total clients, active, expired, expiring soon, and unpaid subscriptions
- **Search** — Search clients by name, business name, phone, or email
- **Filter** — Filter subscriptions by status (Active, Expired, Expiring Soon) and payment status (Paid, Unpaid, Partial)
- **Expiry Alerts** — Highlights subscriptions expiring within 7 days
- **Authentication** — Login/logout to protect all views
- **CSV Export** — Export all subscriptions as a downloadable CSV file
- **Form Validation** — Expiry date cannot be earlier than start date. Amount paid cannot be negative.
- **Automated Tests** — Tests covering active, expired, and expiring soon subscription logic

---

## Tech Stack

- **Backend** — Python 3, Django 5
- **Database** — SQLite
- **Frontend** — Django Templates, Bootstrap 5, Bootstrap Icons

---

## Project Structure

```
subscription_tracker/
├── clients/                  # Client management app
│   ├── migrations/           # Database migrations
│   ├── models.py             # Client model
│   ├── views.py              # CRUD views for clients
│   ├── forms.py              # Client form with Bootstrap styling
│   └── urls.py               # Client URL patterns
├── subscriptions/            # Subscription tracking app
│   ├── migrations/           # Database migrations
│   ├── models.py             # Subscription model with status properties
│   ├── views.py              # CRUD views + CSV export
│   ├── forms.py              # Subscription form with validation
│   ├── tests.py              # Tests for subscription status logic
│   └── urls.py               # Subscription URL patterns
├── dashboard/                # Dashboard app
│   ├── views.py              # Dashboard summary view
│   └── urls.py               # Dashboard URL patterns
├── templates/
│   ├── base.html             # Base layout with sidebar navigation
│   ├── auth/
│   │   └── login.html        # Login page
│   ├── clients/
│   │   ├── client_list.html          # List all clients with search
│   │   ├── client_detail.html        # Single client with subscriptions
│   │   ├── client_form.html          # Add / edit client form
│   │   └── client_confirm_delete.html
│   ├── subscriptions/
│   │   ├── subscription_list.html          # List with filter + CSV export
│   │   ├── subscription_form.html          # Add / edit subscription form
│   │   └── subscription_confirm_delete.html
│   └── dashboard/
│       └── dashboard.html    # Dashboard with stat cards
├── core/                     # Project settings and root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── manage.py
└── README.md
```

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Ab494/subscription-tracker.git
cd subscription-tracker
```

### 2. Create and activate a virtual environment

On Linux/Mac:
```bash
python3 -m venv env
source env/bin/activate
```

On Windows:
```bash
python -m venv env
env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

You will be prompted to enter a username, email, and password.

### 6. Run the development server

```bash
python manage.py runserver
```

### 7. Open in your browser

```
http://127.0.0.1:8000
```

Log in with the superuser credentials you created in step 5.

---

## Running Tests

```bash
python manage.py test subscriptions
```

Expected output:
```
Ran 3 tests in 0.XXXs
OK
```

---

## Usage Guide

### Clients
- Go to **Clients** in the sidebar to view all registered clients
- Click **Add Client** to register a new client
- Use the search bar to find clients by name, business, phone, or email
- Click the eye icon to view a client's full details and their subscriptions
- Click the pencil icon to edit, or the trash icon to delete

### Subscriptions
- Go to **Subscriptions** in the sidebar to view all subscription records
- Click **Add Subscription** to create a new record linked to a client
- Use the status filters — Active, Expiring Soon, Expired
- Use the payment filters — Paid, Unpaid, Partial
- Expiry dates are color coded:
  - Green — Active
  - Orange — Expiring within 7 days
  - Red — Expired
- Click **Export CSV** to download all subscription records as a spreadsheet

### Dashboard
- The dashboard loads automatically after login
- Shows live counts for Total Clients, Active, Expired, Expiring Soon, and Unpaid subscriptions
- The bottom table lists all subscriptions expiring within the next 7 days

---

## Models

### Client
| Field         | Type          | Description                      |
|---------------|---------------|----------------------------------|
| name          | CharField     | Full name of the client          |
| phone_number  | CharField     | Contact phone number             |
| email         | EmailField    | Unique email address             |
| business_name | CharField     | Name of the client's business    |
| status        | CharField     | Active or Inactive               |
| created_at    | DateTimeField | Auto-set on creation             |
| updated_at    | DateTimeField | Auto-updated on every save       |

### Subscription
| Field          | Type          | Description                          |
|----------------|---------------|--------------------------------------|
| client         | ForeignKey    | Linked client (cascades on delete)   |
| start_date     | DateField     | Subscription start date              |
| expiry_date    | DateField     | Subscription expiry date             |
| amount_paid    | DecimalField  | Amount paid in KES                   |
| payment_status | CharField     | Paid / Unpaid / Partial              |
| notes          | TextField     | Optional notes                       |
| created_at     | DateTimeField | Auto-set on creation                 |

---

## Before Deploying to Production

The following changes would be required before deploying this application to a production environment:

1. **Secret Key** — Move `SECRET_KEY` in `settings.py` to an environment variable and never commit it to version control.
2. **Debug Mode** — Set `DEBUG = False` in production. Leaving it `True` exposes sensitive error details to users.
3. **Allowed Hosts** — Update `ALLOWED_HOSTS` to include your actual domain name.
4. **Database** — Replace SQLite with a production-grade database such as PostgreSQL. SQLite is not suitable for concurrent multi-user access.
5. **Static Files** — Run `python manage.py collectstatic` and configure Nginx or WhiteNoise to serve static files.
6. **HTTPS** — Enforce HTTPS using an SSL certificate via Let's Encrypt and Certbot.
7. **Environment Variables** — Store all sensitive config in a `.env` file and load using `python-decouple` or `django-environ`.
8. **Email Configuration** — Configure a real email backend for password resets instead of the default console backend.
9. **Gunicorn** — Replace Django's development server with Gunicorn behind Nginx for production traffic.
10. **Error Logging** — Set up error monitoring using a tool like Sentry to capture and track production errors.

---

## Author

**Evans Cheruiyot**
Full-Stack Developer