import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://user:password@db:5432/lafdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PostgreSQL connection for LISTEN/NOTIFY
    DB_HOST = os.environ.get("DB_HOST", "db")
    DB_PORT = int(os.environ.get("DB_PORT", 5432))
    DB_NAME = os.environ.get("DB_NAME", "lafdb")
    DB_USER = os.environ.get("DB_USER", "user")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

    # Celery configuration
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://redis:6379/0"
    )
