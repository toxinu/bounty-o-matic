"""
Django settings for headhunter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.utils.crypto import get_random_string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'memoize',
    'cachalot',
    'sslserver',
    'social.apps.django_app.default',
    'headhunter.accounts',
    'headhunter.bounties',
    'headhunter.battlenet',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'headhunter.urls'

WSGI_APPLICATION = 'headhunter.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social.backends.battlenet.BattleNetOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = "/"

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Battlenet
SOCIAL_AUTH_BATTLENET_OAUTH2_KEY = ''
SOCIAL_AUTH_BATTLENET_OAUTH2_SECRET = ''


try:
    from .local_settings import *
except ImportError:
    print('!! Warning! File "headhunter/local_settings.py" file is missing')
    print('!! Copy "headhunter/local_settings_example.py" to start a new one')
    raise

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)
DEFAULT_LANGUAGE = 1
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),)
