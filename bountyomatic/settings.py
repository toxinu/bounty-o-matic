"""
Django settings for bountyomatic project.

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
__chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, __chars)

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
    "django.core.context_processors.request",
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
    'cachalot',
    'compressor',
    'social.apps.django_app.default',
    'bountyomatic.accounts',
    'bountyomatic.bounties',
    'bountyomatic.battlenet',
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
    'bountyomatic.middleware.TimezoneMiddleware',
)

GEOIP_PATH = os.path.join(BASE_DIR, "geoip")

ROOT_URLCONF = 'bountyomatic.urls'

WSGI_APPLICATION = 'bountyomatic.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'bountyomatic.accounts.auth.CustomBattleNetOAuth2',
    'bountyomatic.accounts.auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = "/bounty"
SITE_URL = "https://bounty-o-matic.com"
LOGIN_URL = "/login-error"

BATTLENET_API_LOG = os.path.join(BASE_DIR, "battlenet-api.log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s '
                '%(process)d %(thread)d %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'battlenet-api-file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BATTLENET_API_LOG,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'battlenet-api': {
            'handlers': ['battlenet-api-file'],
            'level': 'INFO'
        }
    }
}

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'accounts.User'

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
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',
    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',
    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',
    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',
    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    # 'social.pipeline.user.get_username',
    'bountyomatic.accounts.auth.get_username',
    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',
    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',
    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',
    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',
)

# Battlenet
SOCIAL_AUTH_BATTLENET_OAUTH2_KEY = ''
SOCIAL_AUTH_BATTLENET_OAUTH2_SECRET = ''
BATTLENET_CACHE = {
    'realms': 60 * 60 * 24 * 5,
    'character': 60 * 60 * 24 * 1,
    'guild': 60 * 60 * 24 * 10,
    'player_characters': 60 * 60 * 24 * 3,
    'battletag': 60 * 60 * 24 * 30
}

try:
    from .local_settings import *
except ImportError:
    print('!! Warning! File "bountyomatic/local_settings.py" file is missing')
    print('!! Copy "bountyomatic/local_settings_example.py" to start a new one')
    raise

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en-us', _('English')),
    ('fr-fr', _('French')),
)
DEFAULT_LANGUAGE = 1
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),)


if 'AKISMET_KEY' not in globals():
    raise Exception('Missing AKISMET_KEY in settings')

if 'SITE_URL' not in globals():
    raise Exception('Missing SITE_URL in settings')

if 'RECAPTCHA_SECRET' not in globals():
    raise Exception('Missing RECAPTCHA_SECRET in settings')

if 'RECAPTCHA_KEY' not in globals():
    raise Exception('Missing RECAPTCHA_SECRET in settings')
