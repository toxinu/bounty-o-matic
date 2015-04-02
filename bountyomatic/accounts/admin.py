from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import User
from ..battlenet.api import get_player_battletag


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'battletag', 'email',
        'date_joined', 'last_login', 'is_staff',)

    def battletag(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                reverse('admin:%s_%s_change' % (
                    obj._meta.app_label, obj._meta.module_name),
                    args=(obj.id,)),
                get_player_battletag(obj))
        except:
            return '%s (%s)' % (obj, _("Battletag not found"))
    battletag.allow_tags = True

admin.site.register(User, CustomUserAdmin)
