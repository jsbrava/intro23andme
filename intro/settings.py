"""
Django settings for introduction project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, logging
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# 23andme settings:
CLIENT_ID = os.getenv('CLIENT_ID', "b6736c2125808c87f136100dca6f4c63")
CLIENT_SECRET = os.getenv('CLIENT_SECRET', "dc197e0b270f7b2d461eda7665a23d43")
DEBUG = bool(os.environ.get('DEBUG', False)) # should be True on local dev
DEBUG = False
if DEBUG==True:
    logging.basicConfig(filename='23andme.log',level=logging.DEBUG)
    BASE_URL = "http://0.0.0.0:5000/"
else:
    BASE_URL = "http://stark-wave-7196.herokuapp.com/"

CALLBACK_URL = BASE_URL + "23api/callback"
INTRO_NUM = 1  # number of introductions to send.
ONEMONTH = 31 * 24 * 60 * 60       #a month worth of seconds
WAIT_UPDATE = timedelta(31)        #need to wait about a month before resending updates

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r(lr@p$5l8&a#+8o)mw)9^e#rb6$dz-@w6abe564bx$)j%e@l6'

# SECURITY WARNING: don't run with debug turned on in production!


TEMPLATE_DEBUG = DEBUG


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'members',
    'api',
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'intro.urls'

WSGI_APPLICATION = 'intro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'intro',                      
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'intro_db',
    }
}
"""
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Central'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__),'static').replace('\\','/'),
    os.path.join(BASE_DIR, "static"),
    
)
## the rest is added for Heroku
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config(default="postgres://postgres:admin@127.0.0.1:5432/intro")

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
