"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import dj_database_url
import multiprocessing
from pathlib import Path
from dotenv import load_dotenv
from lib.string import strtobool

if os.path.exists(".env"):
    load_dotenv()

# Set the start method to 'spawn'
multiprocessing.set_start_method('spawn', force=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(strtobool(os.getenv('DEBUG', 'False')))
ALLOWED_HOSTS = [
    '.herokuapp.com',
    'localhost',
    '.voicewriter.app',
    '.voicewriter.pro',
    '.voicewriter.dev'
]

# FILE UPLOADS
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
USER_UPLOADS_PATH = 'user_uploads'
USER_UPLOADS_ROOT = os.path.join(MEDIA_ROOT, USER_UPLOADS_PATH)

FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB

# PYTHON SHELL
SHELL_PLUS = "bpython"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'storages',
    'graphene_django',
    'voice_writer'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# 👇 Add this line here
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'config.urls'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = "/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'common', 'templates'),
            os.path.join(BASE_DIR, 'voice_writer', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,  # Keeps connections open for up to 10 minutes
        )
    }
else:
    raise Exception("DATABASE_URL environment variable not set")

AUTH_USER_MODEL = 'voice_writer.User'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = 'static/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery configuration
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_START_METHOD = os.getenv('CELERY_START_METHOD','fork')

# Celery Beat settings (for periodic tasks)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Storage backend settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Configure Cloudflare R2 credentials and bucket
AWS_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('R2_BUCKET_NAME', 'voice-writer-dev')
AWS_S3_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL', 'https://1144e4c26754e19eb87bbd87012d2227.r2.cloudflarestorage.com')
# Optional: Control file naming
AWS_LOCATION = 'media'

# Optional: Public/Private media settings
AWS_QUERYSTRING_AUTH = True  # Generate signed URLs for private media
AWS_S3_VERIFY = False  # Disable SSL verification for local development
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = None  # Leave as None for Cloudflare R2
AWS_DEFAULT_ACL = None  # Required to avoid issues with public/private access
AWS_S3_FILE_OVERWRITE = False  # Optional: Avoid overwriting files with the same name