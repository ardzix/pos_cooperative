# pos_cooperative
A Point-of-Sale apps for cooperative business using Python and Django-Framework. Featuring investor, product management, sale and reporting. Also support ESC-POS printer and cash drawer.


#### Download:
###### Using git:
```git
git clone https://github.com/ardzix/pos_cooperative.git
```
###### Or download it manualy


#### Installation:
We recommend you to use virtual-environtment to run this app, so your python dependencies won't conflict. Click [here](https://virtualenv.pypa.io/en/stable/) to set your virtual environment.
Either you can use your global python environment.

Since this app is using Django-framework, you can rever to [Django official website](https://www.djangoproject.com/) for intallation and how to run. Either you can follow the installation steps bellow:

* Install the requirements
```shell
pip install -r requirements.txt
```
* Create settings.py file inside pos directory _(pos/settings.py)_ and paste the code bellow into it.
```python
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your_secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
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
TIME_ZONE = 'UTC'
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
    "print_on" : False, // set True if you have your printer connected
    "usb_conf" : {
        "vendor_id" : 0x0483,
        "product_id" : 0x5720,
        "timeout" : 0,
        "input_endpoint" : 0x00,
        "output_endpoint" : 0x02,
    },
    "cut_paper" : False, // set True if you have your printer connected
    "kick_drawer" : False, // set True if you have your printer connected
}

```
* Check your code integrity
```shell
python manage.py check
```
* Migrate your database
```shell
python manage.py makemigrations
python manage.py migrate
```
* Create superuser account
```shell
python manage.py createsuperuser
```


#### Run:
To run the app, you can run this command in shell:
```shell
python manage.py runserver
```
