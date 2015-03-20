from .settings import BASE_DIR
from .settings import INSTALLED_APPS
from .settings import MIDDLEWARE_CLASSES
from .settings import TEMPLATE_CONTEXT_PROCESSORS

SOCIAL_AUTH_BATTLENET_OAUTH2_KEY = ''
SOCIAL_AUTH_BATTLENET_OAUTH2_SECRET = ''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/headhunter_cache',
    }
}
