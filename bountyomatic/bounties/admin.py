from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Bounty
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'battletag', 'character', 'bounty',
        'added_date', 'external', 'is_hidden', )
    list_filter = ('added_date', 'is_hidden', )
    search_fields = ('id', 'character_name', 'character_realm', 'bounty__slug', )
    actions = ('hide_comment', )

    def hide_comment(self, request, queryset):
        queryset.update(is_hidden=True)
    hide_comment.short_description = _("Hide selected comment(s)")

    def battletag(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (
            reverse('admin:%s_%s_change' % (
                    obj.user._meta.app_label, obj.user._meta.model_name),
                    args=(obj.user.id,)),
            obj.user.battletag)
    battletag.allow_tags = True

    def external(self, obj):
        return '<a href="%s#comments" target="_blank">%s</a>' % (
            reverse('bounty-detail', args=(obj.bounty.slug,)),
            _('View'))
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
        'destination', 'destination_faction', 'added_date', 'updated_date',
        'comments_counter', 'is_target_guild', 'is_private', 'is_hidden',
        'external', 'comments_admin', )
    list_filter = (
        'added_date', 'updated_date', 'is_private', 'is_hidden',
        'is_target_guild', 'destination_faction', 'status', 'region', )
    search_fields = (
        'slug', 'source_character', 'source_realm',
        'destination_character', 'destination_realm', )

    def battletag(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                reverse('admin:%s_%s_change' % (
                    obj.user._meta.app_label, obj.user._meta.model_name),
                    args=(obj.user.id,)),
                obj.user.battletag)
        except:
            raise
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

    def comments_admin(self, obj):
        return '<a href="%s?q=%s" target="_blank">%s</a>' % (
            reverse('admin:%s_%s_changelist' % (
                Comment._meta.app_label, Comment._meta.model_name)),
            obj.slug,
            _("View"))
    comments_admin.allow_tags = True
    comments_admin.short_description = _("Admin")

    def external(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (
            reverse('bounty-detail', args=(obj.slug,)),
            _('View'))
    external.allow_tags = True
    external.short_description = _("Context")

admin.site.register(Bounty, BountyAdmin)
admin.site.register(Comment, CommentAdmin)
