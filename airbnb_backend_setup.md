# 🏡 Airbnb Clone Backend Setup - Django + FastAPI

## Architecture Overview

We'll use **Django** for the main application logic, admin interface, and ORM, while **FastAPI** will handle high-performance API endpoints and real-time features.

```
┌─────────────────┐    ┌──────────────────┐
│   Django App    │    │   FastAPI App    │
│   (Core Logic)  │◄──►│  (API Endpoints) │
└─────────────────┘    └──────────────────┘
         │                       │
         └───────────────────────┘
                   │
            ┌─────────────┐
            │ PostgreSQL  │
            │  Database   │
            └─────────────┘
```

## Project Structure

```
airbnb_clone/
├── backend/
│   ├── django_app/
│   │   ├── airbnb_project/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   ├── apps/
│   │   │   ├── authentication/
│   │   │   ├── listings/
│   │   │   ├── bookings/
│   │   │   └── reviews/
│   │   ├── manage.py
│   │   └── requirements-django.txt
│   ├── fastapi_app/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   └── models/
│   │   ├── requirements-fastapi.txt
│   │   └── Dockerfile
│   ├── shared/
│   │   ├── database.py
│   │   └── models.py
│   └── docker-compose.yml
└── README.md
```

## 1. Initial Setup

### Prerequisites
```bash
# Install Python 3.9+, PostgreSQL, and Docker
python --version  # Should be 3.9+
postgres --version
docker --version
```

### Create Project Structure
```bash
mkdir airbnb_clone && cd airbnb_clone
mkdir -p backend/{django_app,fastapi_app,shared}
cd backend
```

## 2. Django Setup

### Install Django Dependencies
```bash
cd django_app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements-django.txt
cat > requirements-django.txt << EOF
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
psycopg2-binary==2.9.8
django-allauth==0.57.0
celery==5.3.4
redis==5.0.1
Pillow==10.1.0
python-decouple==3.8
djangorestframework-simplejwt==5.3.0
stripe==7.8.0
EOF

pip install -r requirements-django.txt
```

### Create Django Project
```bash
django-admin startproject airbnb_project .
cd airbnb_project

# Create apps
python manage.py startapp authentication
python manage.py startapp listings
python manage.py startapp bookings
python manage.py startapp reviews
python manage.py startapp payments
```

### Django Settings Configuration
```python
# airbnb_project/settings.py
import os
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='airbnb_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Applications
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
]

LOCAL_APPS = [
    'authentication',
    'listings',
    'bookings',
    'reviews',
    'payments',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
]

# Celery Configuration (for background tasks)
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Environment Variables (.env)
```bash
# Create .env file in django_app/
cat > .env << EOF
SECRET_KEY=your-very-secret-key-here
DEBUG=True
DB_NAME=airbnb_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
STRIPE_PUBLIC_KEY=pk_test_your_stripe_key
STRIPE_SECRET_KEY=sk_test_your_stripe_key
EOF
```

## 3. FastAPI Setup

### Install FastAPI Dependencies
```bash
cd ../fastapi_app
python -m venv venv
source venv/bin/activate

# Create requirements-fastapi.txt
cat > requirements-fastapi.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.8
alembic==1.12.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
websockets==12.0
redis==5.0.1
pydantic==2.5.0
python-decouple==3.8
httpx==0.25.2
EOF

pip install -r requirements-fastapi.txt
```

### FastAPI Application Structure
```python
# fastapi_app/app/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="Airbnb Clone API",
    description="High-performance API for Airbnb clone",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Airbnb Clone FastAPI Server"}

# WebSocket for real-time messaging
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except:
        pass
```

### FastAPI Configuration
```python
# fastapi_app/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost/airbnb_db"
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Database Connection
```python
# fastapi_app/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 4. Database Setup

### PostgreSQL Database Creation
```bash
# Connect to PostgreSQL and create database
psql -U postgres
CREATE DATABASE airbnb_db;
CREATE USER airbnb_user WITH PASSWORD 'airbnb_password';
GRANT ALL PRIVILEGES ON DATABASE airbnb_db TO airbnb_user;
\q
```

### Django Migrations
```bash
cd django_app
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 5. Docker Setup (Optional)

### Docker Compose Configuration
```yaml
# backend/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: airbnb_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  django:
    build: ./django_app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./django_app:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      - DEBUG=1
      - DB_HOST=postgres
      - REDIS_URL=redis://redis:6379/0

  fastapi:
    build: ./fastapi_app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
    volumes:
      - ./fastapi_app:/app
    ports:
      - "8001:8001"
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

## 6. Running the Applications

### Development Mode
```bash
# Terminal 1: Start PostgreSQL and Redis (if not using Docker)
# Start your local PostgreSQL and Redis services

# Terminal 2: Django Development Server
cd django_app
source venv/bin/activate
python manage.py runserver 8000

# Terminal 3: FastAPI Development Server
cd ../fastapi_app
source venv/bin/activate
uvicorn app.main:app --reload --port 8001

# Terminal 4: Celery Worker (for background tasks)
cd django_app
celery -A airbnb_project worker --loglevel=info
```

### Using Docker
```bash
cd backend
docker-compose up --build
```

## 7. API Integration Between Django and FastAPI

### Shared Database Models
```python
# shared/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "auth_user"  # Django's default user table
    
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    email = Column(String(254))
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime)
```

## 8. Testing the Setup

### Test Django Admin
- Visit: `http://localhost:8000/admin/`
- Login with superuser credentials

### Test FastAPI Docs
- Visit: `http://localhost:8001/docs`
- Interactive API documentation

### Test Database Connection
```bash
# Django shell
cd django_app
python manage.py shell
>>> from django.db import connection
>>> connection.cursor()

# FastAPI test
curl http://localhost:8001/
```

## Next Steps

1. **Implement User Authentication** in Django
2. **Create API endpoints** in FastAPI for high-performance operations
3. **Set up Celery** for background tasks (email sending, image processing)
4. **Implement WebSocket** connections for real-time messaging
5. **Add comprehensive logging** and monitoring
6. **Set up testing framework** (pytest for both Django and FastAPI)

Your backend infrastructure is now ready! You can start implementing the specific features from your project plan.