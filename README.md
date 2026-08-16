# Tea Zone — Restaurant Management System

A Django-based restaurant / tea-house management system with role-based dashboards, order management, room reservations, REST API endpoints, and a Telegram ordering bot.

> **Portfolio note:** This repository is prepared as a demonstration project. It is not configured for production deployment.

## Highlights

- Role-based access for **Director, Manager, Waiter, Cooker, and Call Center** staff
- Custom Django user model with role information
- Restaurant room management and availability tracking
- Food and product inventory management
- Order and order-item workflows
- Delivery order handling
- Client management
- Search and pagination in the management UI
- Django REST Framework API for products, food, rooms, and order creation
- Telegram bot for customer-facing ordering flows
- Admin interface for managing application data
- Configurable secrets through environment variables

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| API | Django REST Framework |
| Database | SQLite for local development |
| Bot | Telegram Bot API via `pyTelegramBotAPI` |
| HTTP client | Requests |
| Frontend | Django Templates, HTML, CSS, JavaScript |
| Authentication | Django authentication + custom `User` model |

## Architecture

```text
                        +----------------------+
                        |   Customer / Staff   |
                        +----------+-----------+
                                   |
                    +--------------+--------------+
                    |                             |
              Web Dashboard                 Telegram Bot
                    |                             |
                    v                             v
             +-------------+              +-------------+
             |    Django   |<-------------|  REST API   |
             |   Web App   |              +-------------+
             +------+------+                     |
                    |                            |
                    +-------------+--------------+
                                  |
                           +------v------+
                           |    SQLite   |
                           +-------------+
```

## Main modules

```text
tea-zone/
├── api/                  # REST API endpoints and serializers
├── bot/                  # Telegram bot
├── main/                 # Domain models, views, admin, migrations
├── templates/            # Dashboard and management UI
├── static/               # Frontend assets
├── teazone/              # Django project configuration
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Roles

| Role | Main responsibility |
|---|---|
| Director | Staff, clients, rooms, products, food, orders, dashboard |
| Manager | Operational management and business overview |
| Waiter | Assigned orders and waiter dashboard |
| Cooker | Order-item processing and kitchen workflow |
| Call Center | Customer/order intake and availability |

The role is stored on the custom Django `User` model and used by the dashboard routing and access checks.

## REST API

Base URL:

```text
http://127.0.0.1:8000/api/
```

Available endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/product/` | List available products |
| GET | `/api/food/` | List available food |
| POST | `/api/room/` | Check room availability for a date |
| POST | `/api/create-order/` | Create a restaurant order |
| POST | `/api/create-delivery/` | Create a delivery order |
| GET | `/api/info/` | Get bot welcome information |
| GET | `/api/detail/` | Get restaurant details |

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/tea-zone.git
cd tea-zone
```

### 2. Create and activate a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and export the variables in your shell.

For a local demo, the defaults in `settings.py` are sufficient for Django itself. The Telegram bot additionally requires `TELEGRAM_BOT_TOKEN`.

Example:

```text
DJANGO_SECRET_KEY=replace-this-with-a-random-secret
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
TELEGRAM_BOT_TOKEN=your_bot_token_here
TEAZONE_API_URL=http://127.0.0.1:8000/api
```

### 5. Create the database

```bash
python manage.py migrate
```

### 6. Create demo data

```bash
python manage.py seed_demo
```

This creates a local demonstration superuser:

```text
Username: ans
Password: 1
```

**Important:** `ans / 1` is intentionally provided only as a local portfolio/demo credential. Do not use it for a public or production deployment.

### 7. Start the web application

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Django admin:

```text
http://127.0.0.1:8000/admin/
```

### 8. Start the Telegram bot

In a second terminal, configure `TELEGRAM_BOT_TOKEN` and run:

```bash
python bot/bot.py
```

The bot communicates with the local Django API.

## Security considerations

The original development copy contained local secrets and a local SQLite database. They are deliberately **not included** in this public-ready version.

The cleaned version:

- removes the local `db.sqlite` database;
- removes the Git history bundled with the uploaded archive;
- moves the Django `SECRET_KEY` to an environment variable;
- moves the Telegram bot token to an environment variable;
- ignores `.env`, local databases, virtual environments, IDE metadata, and Python cache files;
- keeps the demo password only inside a local seed command so the repository itself does not contain a password database.

## What I would improve next

This project is a working portfolio project, but several areas would be good candidates for future engineering work:

- add automated unit/API tests;
- use Django Forms / serializers for stronger validation;
- add authentication/authorization to customer-facing write API endpoints;
- replace integer phone numbers with a string field;
- improve error handling and logging;
- add API documentation (OpenAPI / Swagger);
- containerize the application with Docker;
- move from SQLite to PostgreSQL for production;
- add CI with linting and tests;
- improve date validation and delivery scheduling;
- separate business logic from views;
- add structured configuration for development vs. production.

## Project motivation

Tea Zone was built to solve operational problems in a restaurant environment: staff coordination, room availability, inventory, orders, delivery requests, and customer communication.

The project demonstrates practical backend development rather than only isolated programming exercises: data modeling, authentication, role-based workflows, REST API design, database interaction, and integration with an external messaging platform.

## License

No license is currently specified. Add a license if you decide to distribute the project as open source.
