from .settings import BASE_DIR
from .settings import INSTALLED_APPS
from .settings import MIDDLEWARE_CLASSES
from .settings import TEMPLATE_CONTEXT_PROCESSORS

SOCIAL_AUTH_BATTLENET_OAUTH2_KEY = ''
SOCIAL_AUTH_BATTLENET_OAUTH2_SECRET = ''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/bountyomatic_cache',
    }
}

INSTALLED_APPS += (
    'debug_toolbar',)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'headhunter.middleware.NonHtmlDebugToolbarMiddleware',
)

INTERNAL_IPS = ['127.0.0.1', 'localhost']
