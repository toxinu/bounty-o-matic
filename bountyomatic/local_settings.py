from .settings import BASE_DIR
from .settings import INSTALLED_APPS
from .settings import MIDDLEWARE_CLASSES
from .settings import TEMPLATE_CONTEXT_PROCESSORS

SOCIAL_AUTH_BATTLENET_OAUTH2_KEY = 'ngrhqgbpxu726gqhermjnzxek8hs3ysb'
SOCIAL_AUTH_BATTLENET_OAUTH2_SECRET = 'V3ajydG4dTU7K6rz5dWTCnNdmGnvS94K'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/bountyomatic_cache',
    }
}

INSTALLED_APPS += ('debug_toolbar', )

AKISMET_KEY = "575c1e8c3ceb"
RECAPTCHA_SECRET = "6LeMMgQTAAAAAKAZy2MH03rzYghAsd_x_NX4dVpS"
DEBUG = True
SECRET_KEY = "abcdefghijklmnopqrstuvwxyz0123456789"
