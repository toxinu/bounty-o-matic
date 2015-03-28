from django.contrib import admin

from .models import Bounty
from .models import Comment

admin.site.register(Bounty)
admin.site.register(Comment)
