import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///quiz_master.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = 7200  # 2 hours
    JWT_COOKIE_SECURE = False # Set to True in production
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SAMESITE="Lax"
    JWT_COOKIE_CSRF_PROTECT=False

    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

    MAIL_SERVER = os.getenv("MAIL_SERVER", "mg.csc.tf")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "quizmaster@mg.csc.tf")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "52f3bfd1811f4dd0fd796bf436944ad8-f6202374-93d2f53f")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "21f3002934@ds.study.iitm.ac.in")