"""
Django settings for vogon project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from urlparse import urlparse
from datetime import timedelta
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gtl7=k_#_cx5e9!2(khyq3_#u3=8bh97fi_t0e*p#*u66rwg=&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'autocomplete_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'concepts',
    'annotations',
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'guardian',
    'djcelery',
    'haystack',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'vogon.urls'

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
                'annotations.context_processors.google',
                'annotations.context_processors.version',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

WSGI_APPLICATION = 'vogon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# #
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'vogonweb',
       'USER': 'vogonweb',
       'PASSWORD': 'vogonweb',
       'HOST': 'localhost',
       'PORT': '5432',
   }
}

# TravisCI uses postgres/<blank> by default.
if 'TRAVIS' in os.environ:
    DATABASES['default']['USER'] = 'postgres'
    DATABASES['default']['PASSWORD'] = ''

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_ID = -1

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False

APPEND_SLASH = False
CRISPY_TEMPLATE_PACK = 'bootstrap3'

SUBPATH = ''

JARS_KEY = '050814a54ac5c81b990140c3c43278031d391676'

AUTH_USER_MODEL = 'annotations.VogonUser'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}



# Haystack
# http://django-haystack.readthedocs.org/en/v2.4.0/index.html

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'annotations.elasticsearch_backends.JHBElasticsearch2SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'vogon',
    },
}
if not 'TRAVIS' in os.environ:
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


djcelery.setup_loader()

# AWS Access Key and Secret Key credentials
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', None)
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', None)
S3_BUCKET = os.environ.get('AWS_SECRET_KEY', 'vogonweb-test')

DEFAULT_USER_IMAGE = 'https://s3-us-west-2.amazonaws.com/vogonweb-test/defaultprofile.png'


TEMPORAL_PREDICATES = {
    'start': 'http://www.digitalhps.org/concepts/CONbbbb0940-84be-4450-b92f-557a78249ebd',
    'end': 'http://www.digitalhps.org/concepts/CONbfd1fc2d-0393-4bdb-92f5-7500cdc507f8',
    'occur': 'http://www.digitalhps.org/concepts/ba626314-5d54-41b6-8f41-0013be5269be'
}

PREDICATES = {
    'have': 'http://www.digitalhps.org/concepts/CON83f5110b-5034-4c95-82f8-8f80ff55a1b9',
    'be': 'http://www.digitalhps.org/concepts/CON3fbc4870-6028-4255-9998-14acf028a316'
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'default_cache_table',
    }
}

CONCEPTPOWER_USERID = os.environ.get('CONCEPTPOWER_USERID', None)
CONCEPTPOWER_PASSWORD = os.environ.get('CONCEPTPOWER_PASSWORD', None)
CONCEPTPOWER_ENDPOINT = os.environ.get('CONCEPTPOWER_ENDPOINT', 'http://chps.asu.edu/conceptpower/rest/')
CONCEPTPOWER_NAMESPACE = os.environ.get('CONCEPTPOWER_NAMESPACE', '{http://www.digitalhps.org/}')


QUADRIGA_USERID = os.environ.get('QUADRIGA_USERID', 'test')
QUADRIGA_PASSWORD = os.environ.get('QUADRIGA_PASSWORD', 'test')
QUADRIGA_ENDPOINT = os.environ.get('QUADRIGA_ENDPOINT', 'http://diging-dev.asu.edu:8081/quadriga-test/rest/network')
QUADRIGA_PROJECT = os.environ.get('QUADRIGA_PROJECT', 'ASDF-1234')
QUADRIGA_CLIENTID = os.environ.get('QUADRIGA_CLIENTID', 'vogonweb')

BASE_URI_NAMESPACE = u'http://www.vogonweb.net'




CELERYBEAT_SCHEDULE = {
    'accession_ready_relationsets': {
        'task': 'annotations.tasks.accession_ready_relationsets',
        'schedule': timedelta(seconds=30),
    },
}

CELERY_TIMEZONE = 'UTC'

GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', None)

VERSION = '0.4'
