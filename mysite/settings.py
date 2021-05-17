"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import sys
from pathlib import Path
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lz$ep8(jv3i_h=y2a98qdk-=(fx-txnnqfeh^bs*ui&gkl5!05'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',   # <--
    'buddyfinder',   # <--
    'allauth',   # <--
    'allauth.account',   # <--
    'allauth.socialaccount',   # <--
    'allauth.socialaccount.providers.google',   # <--
    'cloudinary',
    'spotipy',
    'django_private_chat',

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

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if 'test' in sys.argv:
    # Configuration for test database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'd4uq6j6u1q3csm',
            'USER': 'taertumiduiymt',
            'PASSWORD': '860e35a21eddd81b4cd286e2d02d48724e19142c3996aa45f713f8cb4e3cccd7',
            'HOST': 'ec2-107-22-83-3.compute-1.amazonaws.com',
            'PORT': '5432',
            'TEST': {
                'NAME': 'd4uq6j6u1q3csm'
            }
        }
    }
else:
    # Default configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'd1k1kduujisncj',
            'USER': 'gtbdmpdojkujns',
            'PASSWORD': '7a58f221a9da8948b7575a67d8be8d1787c78c3741c14be42fbff04d02256936',
            'HOST': 'ec2-3-221-243-122.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }

d = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(d)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'buddyfinder.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Site id for admin on local
SITE_ID = 7

# Site id for heroku to work
# Comment line to fix social app matching query error locally
SITE_ID = 11

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Activate Django-Heroku.
try:
    # Configure Django App for Heroku.
    # if '/app' in os.environ['HOME']:
    import django_heroku
    django_heroku.settings(locals(), test_runner=False)

except ImportError:
    found = False


cloudinary.config(
    cloud_name="dago6e3dy",
    api_key="439213316165333",
    api_secret="r0_fhOpa_1iHwZc_0700WodbfTg"
)