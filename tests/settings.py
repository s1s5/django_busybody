# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "9995suf$wxqn1!umnv_rn*1@&930lm!tf6o^)50oxktclvffxu"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['tests/templates',
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

ROOT_URLCONF = "tests.urls"


INSTALLED_APPS = [
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    'django.contrib.staticfiles',
    "django_busybody",
    "tests",
    "django_bouncy",
]

SITE_ID = 1

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_busybody.middlewares.GlobalRequestMiddleware',
)
MEDIA_ROOT = 'django_busybody_tests_media_root'
STATICFILES_STORAGE = 'tests.storage.TestStaticStorage'
STATICFILES_DIRS = ['django_busybody_test_static_files_dir']

if django.VERSION >= (1, 10):
    pass
else:
    MIDDLEWARE_CLASSES = MIDDLEWARE

CRYPTO_KEY = 'hoge'
