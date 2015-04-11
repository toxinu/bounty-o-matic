from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _

from .models import User
from ..battlenet.api import refresh_player_cache
from ..battlenet.api import get_player_battletag


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'battletag', 'email',
        'date_joined', 'last_login', 'is_staff',)
    ordering = ('-date_joined', )
    actions = ('refresh_user_data', 'ban_user', )

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

    def ban_user(self, request, queryset):
        for user in queryset.all().only('id'):
            for s in Session.objects.all():
                if s.get_decoded().get('_auth_user_id') == user.id:
                    s.delete()
            user.is_active = False
            user.save()
    ban_user.short_description = _("Ban user")

admin.site.register(User, CustomUserAdmin)
