"""
Django settings for ecs project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os, environ, socket
from boto3 import Session

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_path = environ.Path(__file__)
file_path = os.path.join(BASE_DIR, "devops/envs/local.env")
env = environ.Env()
environ.Env.read_env(file_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hz1$c6dz3$-y9b3d*p$hdp3m36fys93bxjac+xja0cf0axkulr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

def get_ec2_instance_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip


AWS_LOCAL_IP = get_ec2_instance_ip()
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # packages
    'health_check',                             # required
    'health_check.db',                          # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    # 'health_check.contrib.celery',              # requires celery
    # 'health_check.contrib.celery_ping',         # requires celery
    # 'health_check.contrib.psutil',              # disk and memory utilization; requires psutil
    'health_check.contrib.s3boto3_storage',     # requires boto3 and S3BotoStorage backend
    # 'health_check.contrib.rabbitmq',            # requires RabbitMQ broker
    # 'health_check.contrib.redis',               # requires Redis broker

    #custom apps
    'apps.main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DB_HOST'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USERNAME'),
        'PASSWORD': env('DB_PASSWORD'),
        'PORT': env('DB_PORT'),  # Set to empty string for default.
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# S3 bucket configurations
# the media storage configurations
is_s3_enabled = eval(env('S3_ENABLED'))
if is_s3_enabled:
    DEFAULT_FILE_STORAGE = 'conf.storage_backends.MediaStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = env('AWS_LOCATION')
    AWS_LOCATION_MEDIA = env('AWS_LOCATION_MEDIA')
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION_MEDIA)
else:
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
# -----------------------------------------------------------------------
# Cloudwatch config
logger_session = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME,
)
LOG_GROUP = "app-backend-prod-container-log"
STREAM_NAME_INFO = "info.log"

if DEBUG is False:
    LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "aws": {
            "format": (
                u"%(asctime)s [%(levelname)-9s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "info_handler": {
            "level": "INFO",
            "class": "watchtower.CloudWatchLogHandler",
            "boto3_session": logger_session,
            "log_group": LOG_GROUP,
            "stream_name": STREAM_NAME_INFO,
            "formatter": "aws",
        },
    },
    "loggers":{
        "django":{
            "level":"INFO",
            "handlers": ["info_handler"],
            "propagate": True,
        },
    },
}
# -----------------------------------------------------------------------