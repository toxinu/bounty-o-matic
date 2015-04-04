from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import User
from ..battlenet.api import refresh_player_cache
from ..battlenet.api import get_player_battletag


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'battletag', 'email',
        'date_joined', 'last_login', 'is_staff',)
    ordering = ['-date_joined']
    actions = ['refresh_user_data']

    def battletag(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                reverse('admin:%s_%s_change' % (
                    obj._meta.app_label, obj._meta.model_name),
                    args=(obj.id,)),
                get_player_battletag(obj))
        except:
            return '%s (%s)' % (obj, _("Battletag not found"))
    battletag.allow_tags = True

    def refresh_user_data(self, request, queryset):
        for user in queryset.all():
            refresh_player_cache(user)
    refresh_user_data.short_description = _("Refresh user BattleNet data")

admin.site.register(User, CustomUserAdmin)
