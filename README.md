# Crowdfunding Platform

A full-stack crowdfunding platform that connects investors with project owners. The system features a personalized recommendation engine (DeepFM), Stripe payment integration, AI-generated explanations via Google Gemini, and a comprehensive risk profiling system.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework, Python 3.11 |
| Frontend | Angular 16, TypeScript, Chart.js |
| Database | PostgreSQL 15 |
| ML / AI | TensorFlow, XGBoost, scikit-learn, SHAP, Google Gemini |
| Payment | Stripe |
| Container | Docker, Docker Compose |

---

## Features

- **Multi-role system** — Investor, Project Owner, Admin
- **Project lifecycle** — PENDING → OPEN → FUNDED → REPAYING → COMPLETED
- **Personalized recommendations** — DeepFM model with natural language explanations (Gemini + SHAP)
- **Payment processing** — Stripe integration with webhook support
- **Risk profiling** — Questionnaire-based risk assessment for investors
- **Analytics dashboards** — Portfolio report (investor) and revenue report (project owner)
- **Wallet system** — In-platform balance management

---

## Directory Structure

```
Crowdfunding-Platform-main/
│
├── Backend/
│   └── crowdfunding_project/
│       ├── manage.py                   # Django entry point
│       ├── requirements.txt
│       ├── Dockerfile
│       ├── wait-for-db.sh              # Wait for PostgreSQL before starting
│       ├── .env                        # Environment variables (not committed)
│       │
│       ├── crowdfunding_project/       # Django project config
│       │   ├── settings.py
│       │   └── urls.py
│       │
│       ├── accounts/                   # Users, wallets, bank accounts
│       ├── projects/                   # Projects, AI recommendations
│       ├── transactions/               # Investments, Stripe webhooks
│       ├── reports/                    # Revenue & portfolio analytics
│       ├── risk_profiles/              # Risk assessment engine
│       ├── adminpanel/                 # Admin management
│       ├── audit/                      # Audit logging
│       └── interactions/               # User behavior tracking
│
├── crowdfunding-frontend/
│   ├── Dockerfile
│   ├── angular.json
│   ├── package.json
│   └── src/
│       ├── app/
│       │   ├── auth/                   # Login, register
│       │   ├── core/                   # Guards, interceptors, services, models
│       │   ├── features/
│       │   │   ├── landing/
│       │   │   ├── project-listing/
│       │   │   ├── project-detail/
│       │   │   ├── project-owner/
│       │   │   ├── transaction/        # Investment, wallet
│       │   │   ├── reports/            # Portfolio & revenue dashboards
│       │   │   └── risk-profile/
│       │   ├── admin/                  # Admin dashboard
│       │   └── investor/               # Investor dashboard
│       └── environments/
│
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

```
/api/accounts/       → Authentication, registration, wallets
/api/projects/       → Project CRUD, recommendations
/api/transactions/   → Investments, Stripe webhooks
/api/reports/        → Analytics
/api/admin/          → Admin operations
/api/risk-profiles/  → Risk assessment
```

---

## Running with Docker

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A Stripe account (for payment features)
- A Google AI API key (for recommendation explanations)

### 1. Configure environment variables

Create a `.env` file inside `Backend/crowdfunding_project/`:

```env
# Django
SECRET_KEY=your-django-secret-key
DEBUG=True

# PostgreSQL
DB_NAME=crowdfunding
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Google Generative AI
GOOGLE_API_KEY=your_google_api_key
GOOGLE_AI_MODEL=gemini-2.5-flash

# Recommendation settings
RECOMMENDATION_EXPLANATIONS_USE_LLM=True
RECOMMENDATION_EXPLANATIONS_USE_SHAP=False
RECOMMENDATION_SHAP_BACKGROUND_SIZE=20
RECOMMENDATION_SHAP_NSAMPLES=50
```

> **Note:** `DB_HOST` must be `db` (the Docker service name), not `localhost`.

### 2. Build and start all services

```bash
docker compose up --build
```

This starts four services:

| Service | Container | Port | Description |
|---|---|---|---|
| `db` | `postgres_db` | 5432 | PostgreSQL 15 |
| `backend` | `django_backend` | 8080 | Django REST API |
| `frontend` | `angular_frontend` | 4200 | Angular dev server |
| `stripe-cli` | — | — | Local Stripe webhook relay |

### 3. Access the application

| Interface | URL |
|---|---|
| Frontend | http://localhost:4200 |
| Backend API | http://localhost:8080/api/ |
| Django Admin | http://localhost:8080/admin/ |

### 4. Create a superuser (optional)

```bash
docker exec -it django_backend python manage.py createsuperuser
```

### 5. Restore database from backup (optional)

```bash
docker exec -i postgres_db psql -U postgres -d crowdfunding < crowdfunding.backup
```

---

## Running in Development (without Docker)

### Backend

```bash
cd Backend/crowdfunding_project
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd crowdfunding-frontend
npm install
ng serve
```

---

## Useful Docker Commands

```bash
# Start services in the background
docker compose up -d

# Stop all services
docker compose down

# Stop and remove volumes (resets database)
docker compose down -v

# View backend logs
docker logs -f django_backend

# Run Django management commands
docker exec -it django_backend python manage.py <command>
```
