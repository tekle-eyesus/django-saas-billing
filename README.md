# SaaS API

[![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red?style=for-the-badge)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**SaaS billing API** is a production-ready backend engine designed for scalable subscription management. It features a multi-tenant architecture, role-based access control (RBAC), and a robust billing system integrated with **Chapa**.

Built with **Django REST Framework**, this API demonstrates how to handle real-world SaaS challenges like dynamic rate limiting, secure webhook processing, and automated subscription status tracking.

---

## ⚡ Key Features

### 🏢 Multi-Tenancy & RBAC
- **Organization-First Architecture:** Users belong to Organizations (Teams).
- **Role-Based Access Control:** Granular permissions for `OWNER`, `ADMIN`, and `MEMBER`.
- **JWT Authentication:** Secure stateless authentication using `SimpleJWT`.

### 💳 Billing & Subscriptions
- **Plan Management:** Flexible tier system (e.g., Free, Pro, Enterprise).
- **Chapa Integration:** Secure payment initialization and transaction tracking.
- **Webhook Listener:** HMAC-signed webhook verification to auto-renew subscriptions upon successful payment.
- **Idempotency:** Prevents duplicate processing of payment events.

### 🛡️ Security & Performance
- **Dynamic Rate Limiting:** API quotas are enforced based on the active subscription plan (e.g., Free: 10 req/day, Pro: 10k req/day).
- **Dockerized:** Fully containerized setup with PostgreSQL and Redis.
- **Swagger Documentation:** Automated, interactive API docs via `drf-spectacular`.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12, Django 5, Django REST Framework
- **Database:** PostgreSQL (Production), SQLite (Dev)
- **Caching & Throttling:** Redis
- **Containerization:** Docker, Docker Compose
- **Server:** Gunicorn
- **Documentation:** OpenAPI 3.0 (Swagger UI)

---

## 📂 Project Structure

A modular, scalable folder structure designed for growth.

```text
nexus_saas/
├── apps/
│   ├── analytics/      # Usage tracking & Dashboard endpoints
│   ├── billing/        # Chapa/Stripe logic, Webhooks, Transactions
│   ├── common/         # Shared utilities
│   ├── organizations/  # Tenant management
│   ├── subscriptions/  # Plans, Quotas, Throttling logic
│   └── users/          # Auth, RBAC, Profiles
├── config/             # Project settings (Base, Local, Production)
├── docker-compose.yml  # Orchestration
├── Dockerfile          # Image definition
└── manage.py
```
## 🚀 Getting Started

### Option 1: Run with Docker (Recommended)

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/nexus-saas.git
cd nexus-saas
```
### 2. Create Environment Variables

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Docker Service Name)
DB_HOST=db
DB_NAME=saas_db
DB_USER=postgres
DB_PASSWORD=postgres

# Redis
REDIS_HOST=redis

# Payment Gateway (Chapa)
CHAPA_SECRET_KEY=CHASECK_TEST-xxxxxxxxxxxx
CHAPA_WEBHOOK_SECRET=your-webhook-secret
```
### 3. Build and Run

```bash
docker-compose up --build
```
### 4. Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```
### Option 2: Run Locally (Virtual Environment)

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
### 2. Configure Database

Update `.env` to remove `DB_HOST` (defaults to SQLite) or set it to `localhost` if using local PostgreSQL.

### 3. Run Migrations & Server

```bash
python manage.py migrate
python manage.py runserver
```
## 📖 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/

## 🧪 Testing the Payment Flow

Since Chapa cannot reach localhost for webhooks, you can simulate the flow:

1. Register a user and organization via **/api/auth/register/**.
2. Login to get your **JWT Access Token**.
3. Initiate Payment via **/api/billing/initiate/** with a plan slug (e.g., `pro`).
4. Simulate Webhook using Postman:
   - **POST** to `/api/billing/webhook/chapa/`
   - **Body:**

```json
{
  "event": "charge.success",
  "tx_ref": "YOUR_TX_REF_FROM_STEP_3",
  "data": { "tx_ref": "...", "amount": "500" }
}
```
5. Check **/api/analytics/dashboard/** to see your rate limits updated!

## 🤝 Contributing
Contributions are welcome! Please fork the repository and open a pull request.

## 📄 License
This project is licensed under the **MIT License**.

