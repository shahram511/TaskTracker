# 📋 Task Tracker API

A robust and production-ready Task Management API built with **Django REST Framework**.
This project features advanced authentication, background task processing, and a scalable architecture.

## 🚀 Key Features

* **Custom Authentication:** Login using **Phone Number** (instead of username) & JWT Tokens.
* **Task Management:** Create, Read, Update, Delete (CRUD) tasks.
* **Categorization:** Organize tasks into custom Categories.
* **Smart Filtering:** Filter tasks by status, priority, category, or search by title.
* **Background Jobs:** Asynchronous email reminders using **Celery & Redis**.
* **Scheduled Reminders:** Automated daily emails for tasks due tomorrow.
* **One-Click Actions:** Custom endpoints to quickly mark tasks as 'Done'.
* **Docker Ready:** Includes Dockerfile and Docker Compose for containerized deployment.

## 🛠 Tech Stack

* **Backend:** Python 3.12, Django 5, Django REST Framework
* **Database:** PostgreSQL (Production) / SQLite (Development)
* **Async Task Queue:** Celery 5
* **Message Broker:** Redis
* **Security:** JWT (Simple JWT), Python-Decouple

---

## 💻 Installation & Setup (Windows)

Follow these steps to run the project locally without Docker.

### 1. Prerequisites
* Python 3.12+
* [Redis for Windows](https://github.com/tporadowski/redis/releases) (Must be installed and running)

### 2. Clone the Repository
```bash
git clone https://github.com/shahram511/TaskTracker.git
cd TaskTracker
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables
Create a `.env` file or configure your settings to include:
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Run The Application
You need to open **3 separate terminals** to run the full stack:

**Terminal 1: Django Server**
```bash
python manage.py runserver
```
*Access API at: http://127.0.0.1:8000/api/docs/*

**Terminal 2: Celery Worker**
```bash
celery -A config worker --pool=solo -l info
```

**Terminal 3: Celery Beat (Scheduler)**
```bash
celery -A config beat -l info
```

---

## 🐳 Running with Docker

Alternatively, you can run the entire stack with a single command:

```bash
docker-compose up --build
```

---

## 📚 API Documentation

Once the server is running, you can explore the interactive API docs:

* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
* **Redoc:** `http://127.0.0.1:8000/api/schema/`
```