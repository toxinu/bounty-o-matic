from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import SimpleListFilter

from .models import User
from ..battlenet.api import get_player_battletag
from ..battlenet.api import refresh_player_cache


class NullBattleTagFilter(SimpleListFilter):
    title = _('BattleTag')
    parameter_name = 'battletag'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Has value'), ),
            ('0', _('None'), ),
        )

    def queryset(self, request, queryset):
        kwargs = {self.parameter_name: None}
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'battletag', 'date_joined', 'last_login',
        'is_staff', 'is_active', 'battlenet_error')
    list_filter = (NullBattleTagFilter, 'is_active', 'is_superuser', 'is_staff', )
    ordering = ('-date_joined', )
    actions = ('refresh_user_data', 'ban_user', 'new_social_auth', )

    def battletag(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                reverse('admin:%s_%s_change' % (
                    obj._meta.app_label, obj._meta.model_name),
                    args=(obj.id,)),
                obj.battletag)
        except:
            return '%s (%s)' % (obj, _("Battletag not found"))
    battletag.allow_tags = True

    def battlenet_error(self, obj):
        if not obj.battletag:
            battletag, error = get_player_battletag(obj)
            return error
    battlenet_error.short_description = _('BattleNet error')

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

    def new_social_auth(self, request, queryset):
        for user in queryset.all():
            if hasattr(user, 'social_auth') and user.social_auth.exists():
                user.social_auth.all().delete()
    new_social_auth.short_description = _("Force new BattleNet authentication")

admin.site.register(User, CustomUserAdmin)
