from __future__ import absolute_import

import os
import django
from carotte import Carotte

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bountyomatic.settings')
django.setup()

app = Carotte()

from .battlenet import tasks
