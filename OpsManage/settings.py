"""
Django settings for OpsManage project.

Generated by 'django-admin startproject' using Django 1.9.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import djcelery
from celery import  platforms
from kombu import Queue,Exchange
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

''' celery config '''
djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/4'
CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER='pickle'
CELERY_ACCEPT_CONTENT = ['pickle','json']
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERYD_MAX_TASKS_PER_CHILD = 40
CELERY_TRACK_STARTED = True
CELERY_TIMEZONE='Asia/Shanghai'
platforms.C_FORCE_ROOT = True

#celery route config
CELERY_IMPORTS = ("OpsManage.tasks.assets","OpsManage.tasks.ansible",
                  "OpsManage.tasks.cron","OpsManage.tasks.deploy",
                  "OpsManage.tasks.sql","OpsManage.tasks.sched")
CELERY_QUEUES = (
    Queue('default',Exchange('default'),routing_key='default'),
    Queue('ansible',Exchange('ansible'),routing_key='ansible_#'),
)
CELERY_ROUTES = {
    'OpsManage.tasks.ansible.AnsibleScripts':{'queue':'ansible','routing_key':'ansible_scripts'},
    'OpsManage.tasks.ansible.AnsiblePlayBook':{'queue':'ansible','routing_key':'ansible_playbook'},
}
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'



REDSI_KWARGS_LPUSH = {"host":'127.0.0.1','port':6379,'db':3}
REDSI_LPUSH_POOL = None
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kd8f&jx1h^1m-uldfdo3d#10d9mbc-ijjz!tozusy@aw#h+875'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Channels settings
CHANNEL_LAYERS = {
    "default": {
       "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
       "CONFIG": {
           "hosts": [("localhost", 6379)],  # set redis address
           "channel_capacity": {
                                   "http.request": 1000,
                                   "websocket.send*": 10000,
                                },
           "capacity": 10000,
           },
       "ROUTING": "OpsManage.routing.channel_routing",  # load routing from our routing.py file
       },
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'OpsManage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#     'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
#     ),              
#}


ROOT_URLCONF = 'OpsManage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["/opt/ops/OpsManage/static/",'/mnt/OpsManage/OpsManage/templates/'],
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


WSGI_APPLICATION = 'OpsManage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'ops',
        'USER':'ops',
        'PASSWORD':'1234',
        'HOST':'127.0.0.1',
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
     '/opt/ops/OpsManage/static/',
    )
TEMPLATE_DIRS = (
# #     os.path.join(BASE_DIR,'mysite\templates'),
     '/opt/ops/OpsManage/templates/',
 )


LOGIN_URL = '/login'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
             'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'filters': {
    },
    'handlers': {
         'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'tofile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter':'standard',
            'filename': '/opt/ops/OpsManage/logs/ns_oper.log',
        },
    },
    'loggers': {
        'ops.Opsmanage': {
            'handlers': ['tofile'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
