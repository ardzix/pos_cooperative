"""
Django settings for pos project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o#cj1=ho8pjx5w%!5z*ak&4u=kynxv-zw76+xa2ubq0x(z0bq6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'pos_core.apps.PosCoreConfig',
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',

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

ROOT_URLCONF = 'pos.urls'

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

WSGI_APPLICATION = 'pos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pos',
        'USER': 'postgres',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

PHOTO_FOLDER = ''
BARCODE_FOLDER = ''
VIDEO_FOLDER = ''
BACKGROUND_COVER_FOLDER = ''
AVATAR_FOLDER = ''
LOGO_FOLDER = ''
IDENTITY_FOLDER = ''
PHOTO_SIZES = ()
SITE_ID = 1
PAGE_RANGE_TOP_NUM = 5
PAGE_RANGE_BOTTOM_NUM = 5

EXCLUDE_FORM_FIELDS = (
    "id", "id62", "site", "nonce",
    "created_at", "created_at_timestamp", "created_by",
    "updated_at", "updated_at_timestamp", "updated_by",
    "published_at", "published_at_timestamp", "published_by",
    "unpublished_at", "unpublished_at_timestamp", "unpublished_by",
    "approved_at", "approved_at_timestamp", "approved_by",
    "unapproved_at", "unapproved_at_timestamp", "unapproved_by",
    "deleted_at", "deleted_at_timestamp", "deleted_by",
)

# Printer Settings
PRINTER_CONF = {
    "print_on" : False,
    "usb_conf" : {
        "vendor_id" : 0x0483,
        "product_id" : 0x5720,
        "timeout" : 0,
        "input_endpoint" : 0x00,
        "output_endpoint" : 0x02,
    },
    "cut_paper" : True,
}
