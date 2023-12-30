"""
Django settings for Werknemersapp project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from telnetlib import AUTHENTICATION
from click import INT
from django.urls import reverse_lazy
from datetime import timedelta
import os
from dotenv import load_dotenv
from sympy import false
load_dotenv()  # This loads the variables from .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9efm@rcp(9f@cshbf+z7b))i!hhrovtjh4gkj9v=5^t$qgg@1y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["178.79.150.108", "178-79-150-108.ip.linodeusercontent.com", "lvs.schoolklaar.nl", "127.0.0.1", "localhost"]



# Application definition
INSTALLED_APPS = [
    'rest_framework',                # Provides tools to build Web APIs in Django
    "crispy_bootstrap4",            # Plugin to work with Bootstrap 4 in crispy_forms
    'crispy_forms',                 # Helps to manage Django forms
    "rest_framework.authtoken",     # Token-based authentication for REST framework
    'Login.apps.MyAppConfig',       # Custom app for handling user login
    'authentication.apps.AuthenticationConfig', # Custom app for user authentication
    "rest_framework_simplejwt",     # Handles JWT authentication
    'django.contrib.admin',         # Built-in Django admin interface
    'django.contrib.auth',          # Built-in user authentication system
    'django.contrib.contenttypes',  
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'tailwind',                     # Utility-first CSS framework
    'theme',                        # Custom theming app
    'django_browser_reload',        # Auto-reloading browser when code changes
    'corsheaders',                  # Handles Cross-Origin Resource Sharing headers
    "allauth",                      # Authentication app
    "allauth.account",              # Core of allauth
    "allauth.socialaccount",        # Provides social authentication
    "dj_rest_auth",                 # REST authentication
    "dj_rest_auth.registration",    # Handles user registration via REST
    "allauth.socialaccount.providers.google",  # Google OAuth provider
]


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "888008928753-qntnk84kepfj66t89g69lijrtmmamvng.apps.googleusercontent.com",  # replace me
            "secret": "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",        # replace me
            "key": "",                               # leave empty
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "VERIFIED_EMAIL": True,
    },
}
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ["127.0.0.1",]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Add this line
    'corsheaders.middleware.CorsMiddleware', # new
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
  
    
]



ROOT_URLCONF = 'Werknemersapp.urls'


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", # If your frontend is served on localhost:3000 during development
    "https://yourfrontenddomain.com",
    "https://leerlingportaal-frontend.vercel.app",
    "https://schoolklaar-fronend-backend.vercel.app",
    "https://payments-dashboard-rose.vercel.app",
    
 ]
CORS_ALLOW_CREDENTIALS = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'Werknemersapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


LANGUAGE_CODE = 'nl'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

#STATIC_URL = STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#MEDIAURL


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

DATE_INPUT_FORMATS =  ['%d/%m/%Y']

LOGIN_REDIRECT_URL=reverse_lazy('Login:add_sessie')
LOGOUT_REDIRECT_URL = 'login'

SESSION_COOKIE_AGE_REMEMBER_ME = 60 * 60 * 24 * 30  # 30 days in seconds
SESSION_COOKIE_HTTPONLY = True

CSRF_HEADER_NAME = 'X-CSRFToken'
CSRF_HEADER_NAME = 'HTTP_X-CSRFToken'


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": "complexsigningkey",  # generate a key and replace me
    "ALGORITHM": "HS512",
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}


SITE_ID = 2

ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"


REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
}


if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000/",
        "http://127.0.0.1:3000/",
        "https://leerling.schoolklaar.nl/",
        "http://localhost:3000/",
        "https://schoolklaar-fronend-backend.vercel.app",
        "https://leerlingportaal-frontend.vercel.app/"
    ]




DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'sqlite')

if DATABASE_TYPE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME', 'default_db_name'),
            'USER': os.environ.get('DB_USER', 'default_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'default_password'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'OPTIONS': {
                'sslmode': 'disable',
            },
        }
    }
else:  # Default to SQLite if DATABASE_TYPE is not 'postgres'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
