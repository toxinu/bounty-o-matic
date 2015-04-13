from __future__ import absolute_import

import os
from carotte import Carotte

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bountyomatic.settings')

app = Carotte()
