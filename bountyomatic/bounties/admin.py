from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Bounty
from .models import Comment

from ..battlenet.api import get_player_battletag


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'battletag', 'character', 'bounty',
        'added_date', 'is_hidden', 'external',)
    list_filter = ('added_date', 'is_hidden', )

    def battletag(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (
            reverse('admin:%s_%s_change' % (
                    obj.user._meta.app_label, obj.user._meta.module_name),
                    args=(obj.user.id,)),
            get_player_battletag(obj.user))
    battletag.allow_tags = True

    def external(self, obj):
        return '<a href="%s#comments" target="_blank">%s</a>' % (
            reverse('bounty-detail', args=(obj.bounty.pk,)),
            'View')
    external.allow_tags = True
    external.short_description = _("Context")

    def character(self, obj):
        return '<a href="%s" target="_blank">%s - %s</a>' % (
            obj.character_armory,
            obj.character_name,
            obj.get_character_realm_display())
    character.allow_tags = True


class BountyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'battletag', 'status', 'region', 'source',
        'destination', 'added_date', 'updated_date',
        'comments_counter', )
    list_filter = ('added_date', 'updated_date', 'is_private', 'status', )

    def battletag(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                reverse('admin:%s_%s_change' % (
                    obj.user._meta.app_label, obj.user._meta.module_name),
                    args=(obj.user.id,)),
                get_player_battletag(obj.user))
        except:
            return '%s (%s)' % (obj.user, _("Battletag not found"))
    battletag.allow_tags = True

    def source(self, obj):
        return '<a href="%s" target="_blank">%s - %s</a>' % (
            obj.source_armory,
            obj.source_character, obj.get_source_realm_display())
    source.allow_tags = True

    def destination(self, obj):
        return '<a href="%s" target="_blank">%s - %s</a>' % (
            obj.destination_armory,
            obj.destination_character, obj.get_destination_realm_display())
    destination.allow_tags = True

    def comments_counter(self, obj):
        return obj.comment_set.count()
    comments_counter.short_description = _("Comments")

admin.site.register(Bounty, BountyAdmin)
admin.site.register(Comment, CommentAdmin)
