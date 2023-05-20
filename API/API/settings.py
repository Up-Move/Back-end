"""
Django settings for API project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-518-4&30kc0i)w8yrms^c!j9+4qepuw08h#a78szx*sy8d(!8f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ACCOUNT_EMAIL_VERIFICATION = 'none'

#ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dj_rest_auth',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
<<<<<<< HEAD
    'rest_framework_swagger',
    'drf_spectacular'
=======
    'corsheaders',
    'sslserver',
>>>>>>> dd62d532884d3c30a8acf2060784241b3cb67b9f
]

CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ['0.0.0.0,18.205.155.235']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
       # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny',
    ]
}

#CORS_ALLOW_ALL_ORIGINS: True
CORS_ORIGIN_ALLOW_ALL = True
#CORS_REPLACE_HTTPS_REFERER      = False
#HOST_SCHEME                     = "http://"
#SECURE_PROXY_SSL_HEADER         = None
#SECURE_SSL_REDIRECT             = False
#SESSION_COOKIE_SECURE           = False
#CSRF_COOKIE_SECURE              = False
#SECURE_HSTS_SECONDS             = None
#SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
#SECURE_FRAME_DENY               = False

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    "corsheaders.middleware.CorsMiddleware",
#    "django.middleware.common.CommonMiddleware",

]

ROOT_URLCONF = 'API.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'API.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
<<<<<<< HEAD
        'ENGINE': 'django.db.backends.postgresql',
=======
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
>>>>>>> dd62d532884d3c30a8acf2060784241b3cb67b9f
        'NAME': 'Grupo1_PostgreSQL_DB',
        'USER': 'Grupo1',
        'PASSWORD': 'IFSP2023!',
        'HOST': 'grupo1-postgresql.crys2li8ehue.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

<<<<<<< HEAD
=======
CSRF_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = [
    'http://0.0.0.0',
    'http://18.205.155.235',
    'http://localhost',
    'https://intranet.srv.xxx.eu',
    'https://intranet-staging.srv.xxx.eu',
]

CORS_REPLACE_HTTPS_REFERER = True
>>>>>>> dd62d532884d3c30a8acf2060784241b3cb67b9f
