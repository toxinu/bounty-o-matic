import uuid
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .utils import markdown
from ..storage import OverwriteStorage
from ..battlenet.api import CLASSES
from ..battlenet.api import FACTIONS
from ..battlenet.api import get_character
from ..battlenet.api import get_pretty_realm
from ..battlenet.api import is_player_character
from ..battlenet.api import is_guild_exists
from ..battlenet.api import is_character_exists
from ..battlenet.api import get_guild_armory
from ..battlenet.api import get_character_armory
from ..battlenet.api import get_character_thumbnail
from ..battlenet.api import get_character_thumbnail_fallback
from ..battlenet.api import get_guild_thumbnail


class Bounty(models.Model):
    REGION_EU = 'eu'
    REGION_US = 'us'
    # REGION_KR = 'kr'
    # REGION_TW = 'tw'
    REGION_CHOICES = (
        (REGION_EU, _('Europe')),
        (REGION_US, _('US')), )
    # (REGION_KR, _('Korea')),
    # (REGION_TW, _('Taiwan')),)

    STATUS_OPEN = 1
    STATUS_CLOSE = 2
    STATUS_CANCELLED = 3
    STATUS_CHOICES = (
        (STATUS_OPEN, _('Open')),
        (STATUS_CLOSE, _('Closed')),
        (STATUS_CANCELLED, _('Cancelled')),)

    FACTION_ALLIANCE = 0
    FACTION_HORDE = 1
    FACTION_NEUTRAL = 2
    FACTION_CHOICES = (
        (FACTION_ALLIANCE, FACTIONS[FACTION_ALLIANCE]),
        (FACTION_HORDE, FACTIONS[FACTION_HORDE]),
        (FACTION_NEUTRAL, FACTIONS[FACTION_NEUTRAL]),)

    ################
    # Informations #
    ################
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    reward = models.TextField(verbose_name=_("Reward"))
    description = models.TextField(verbose_name=_("Description"))
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=STATUS_OPEN, verbose_name=_("Status"))
    region = models.CharField(
        max_length=2, choices=REGION_CHOICES, default=REGION_EU, verbose_name=_("Region"))
    added_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("Latest update"))

    is_private = models.BooleanField(default=False, verbose_name=_('Private'))
    comments_closed = models.BooleanField(
        default=False, verbose_name=_('Comments closed'))
    comments_closed_by_staff = models.BooleanField(
        default=False, verbose_name=_('Comments closed by staff'))
    is_target_guild = models.BooleanField(
        default=False, verbose_name=_("Target guild"))
    slug = models.UUIDField(default=uuid.uuid4, unique=True)
    is_hidden = models.BooleanField(default=False, verbose_name=_("Hidden"))

    ##########
    # Source #
    ##########

    source_realm = models.CharField(max_length=50, verbose_name=_("Source realm"))
    source_character = models.CharField(max_length=50, verbose_name=_("Source character"))

    ###############
    # Destination #
    ###############
    destination_realm = models.CharField(
        max_length=50, verbose_name=_("Target realm"), null=True)
    destination_character = models.CharField(
        max_length=50, verbose_name=_("Target name"), null=True)
    destination_faction = models.PositiveSmallIntegerField(
        choices=FACTION_CHOICES, verbose_name=_("Faction"), null=True)

    ##########
    # Winner #
    ##########
    winner_realm = models.CharField(
        max_length=50, verbose_name=_("Winner realm"), null=True, blank=True)
    winner_character = models.CharField(
        max_length=50, verbose_name=_("Winner character"), null=True, blank=True)

    class Meta:
        verbose_name_plural = _('bounties')
        ordering = ['-updated_date']
        unique_together = ((
            'user', 'source_realm', 'source_character',
            'destination_realm', 'destination_character'),)

    def __str__(self):
        return "[%s] %s - %s by %s - %s" % (
            self.region,
            self.destination_character,
            self.get_destination_realm_display(),
            self.source_character,
            self.get_source_realm_display())

    def clean(self):
        # Delay between creating bounties
        if not self.user.is_staff and Bounty.objects.filter(
                user=self.user,
                added_date__gte=timezone.make_aware(
                    datetime.datetime.now(),
                    timezone.get_current_timezone()) - datetime.timedelta(
                        minutes=3)).exists() and self.pk is None:
            raise ValidationError(_(
                "Bounty limit reached. Wait before sending a new one. "
                "Something like 3 minutes..."))

        try:
            previous_obj = Bounty.objects.get(pk=self.pk)
        except Bounty.DoesNotExist:
            previous_obj = Bounty.objects.none()

        # Check status workflow
        if self.pk is not None:
            if previous_obj.status in [self.STATUS_CLOSE, self.STATUS_CANCELLED]:
                if self.status == self.STATUS_OPEN:
                    raise ValidationError(_("Bounty can't be re-open. Create a new one."))
            if self.status in [self.STATUS_CANCELLED, self.STATUS_OPEN]:
                self.winner_realm = None
                self.winner_character = None

        # Destination checks (if not a guild)
        if not self.is_target_guild:
            exists, destination = is_character_exists(
                self.region, self.destination_realm, self.destination_character)
            if not exists and self.pk is None or not exists and (
                    (self.destination_realm, self.destination_character) !=
                    (previous_obj.destination_realm, previous_obj.destination_character)):
                raise ValidationError(
                    _("Target character does not exist or is below level 10."))
            if exists:
                self.destination_character = destination.get('name')
                self.destination_faction = destination.get('faction')
        # If it's a guild
        else:
            exists, destination = is_guild_exists(
                self.region, self.destination_realm, self.destination_character)
            if not exists and self.pk is None or not exists and (
                    (self.destination_realm, self.destination_character) !=
                    (previous_obj.destination_realm, previous_obj.destination_character)):
                raise ValidationError(
                    _("Target guild does not exist."))
            if exists:
                self.destination_character = destination.get('name')
                self.destination_faction = destination.get('side')

        # Source checks
        exists, source = is_character_exists(
            self.region, self.source_realm, self.source_character)
        if not exists and self.pk is None or not exists and (
                (self.source_realm, self.source_character) !=
                (previous_obj.source_realm, previous_obj.source_character)):
            raise ValidationError(
                _("Your character is below level 10 or on an inactive account."))
        if exists:
            self.source_character = source.get('name')

        if not is_player_character(
                self.user,
                self.source_character,
                self.source_realm, self.region) and self.pk is None:
            raise ValidationError(_("This character is not yours."))

        # Winner checks
        if self.winner_realm and self.winner_realm:
            # Winner character must be different than bounty source
            if self.winner_realm == self.source_realm \
                    and self.winner_character == self.source_character:
                raise ValidationError(_("Winner character can't be bounty author."))
            # Winner character must be different
            # that bounty target (if target is not a guild)
            if self.winner_realm == self.destination_realm \
                    and self.winner_character == self.destination_character \
                    and not self.is_target_guild:
                raise ValidationError(_("Winner character can't be bounty target."))
            exists, winner = is_character_exists(
                self.region, self.winner_realm, self.winner_character)
            # Winner character must exists or the same as previous
            if not exists and self.pk is None or not exists and (
                    (self.winner_realm, self.winner_character) !=
                    (previous_obj.winner_realm, previous_obj.winner_character)):
                raise ValidationError(
                    _("Winner character does not exist or is below level 10."))
            # Winner character can't be bounty owner's characters
            if is_player_character(
                    self.user, self.winner_character, self.winner_realm, self.region):
                raise ValidationError(_("Winner character can't be yours."))

            # If winner is ok, set status to self.STATUS_CLOSE
            self.status = self.STATUS_CLOSE
            self.winner_character = winner.get('name')
            self.winner_realm = self.winner_realm.strip()

        self.source_realm = self.source_realm.strip()
        self.destination_realm = self.destination_realm.strip()

        if not self.is_target_guild:
            # Check source and destination are different
            if self.source_realm == self.destination_realm:
                if self.source_character == self.destination_character:
                    raise ValidationError(
                        _("Your character and target must be different."))
        else:
            source_guild_name = source.get('guild', {}).get('name',)
            source_guild_realm = source.get('guild', {}).get('realm')
            destination_guild_name = destination.get('guild', {}).get('name')
            destination_guild_realm = destination.get('guild', {}).get('realm')
            if (source_guild_name and source_guild_realm) and \
                    (destination_guild_name and destination_guild_realm):
                if (source_guild_name and source_guild_realm) == \
                        (destination_guild_name and destination_guild_realm):
                    raise ValidationError(_("Your guild target can't be your guild."))

        self.region = self.region.lower()

    def get_source_realm_display(self):
        return get_pretty_realm(self.source_realm)

    def get_destination_realm_display(self):
        return get_pretty_realm(self.destination_realm)

    def get_winner_realm_display(self):
        return get_pretty_realm(self.destination_realm)

    @property
    def source_detail(self):
        return get_character(self.region, self.source_realm, self.source_character) or {}

    @property
    def destination_detail(self):
        return get_character(
            self.region, self.destination_realm, self.destination_character) or {}

    @property
    def winner_detail(self):
        if not self.winner_realm or not self.winner_character:
            return {}
        return get_character(
            self.region, self.winner_realm, self.winner_character) or {}

    @property
    def source_thumbnail(self):
        return get_character_thumbnail(
            self.region, self.source_realm, self.source_character)

    @property
    def source_thumbnail_fallback(self):
        return get_character_thumbnail_fallback(
            self.region, self.source_realm, self.source_character)

    @property
    def destination_thumbnail(self):
        if self.is_target_guild:
            return get_guild_thumbnail(
                self.region, self.destination_realm, self.destination_character)
        return get_character_thumbnail(
            self.region, self.destination_realm, self.destination_character)

    @property
    def destination_thumbnail_fallback(self):
        if self.is_target_guild:
            return get_guild_thumbnail(
                self.region, self.destination_realm, self.destination_character)
        return get_character_thumbnail_fallback(
            self.region, self.destination_realm, self.destination_character)

    @property
    def destination_armory(self):
        if self.is_target_guild:
            return get_guild_armory(
                self.region, self.destination_realm, self.destination_character)
        return get_character_armory(
            self.region, self.destination_realm, self.destination_character)

    @property
    def source_armory(self):
        return get_character_armory(
            self.region, self.source_realm, self.source_character)

    @property
    def winner_armory(self):
        if not self.winner_realm or not self.winner_character:
            return
        return get_character_armory(
            self.region, self.winner_realm, self.winner_character)

    @property
    def source_faction_display(self):
        return str(FACTIONS.get(self.source_detail.get('faction', ''), '')) or None

    @property
    def winner_faction_display(self):
        return str(FACTIONS.get(self.winner_detail.get('faction', ''), '')) or None

    @property
    def source_class_display(self):
        return str(CLASSES.get(self.source_detail.get('class', ''), '')) or None

    @property
    def destination_class_display(self):
        return str(CLASSES.get(self.destination_detail.get('class', ''), '')) or None

    @property
    def winner_class_display(self):
        return str(CLASSES.get(self.winner_detail.get('class', ''), '')) or None

    @property
    def source_guild(self):
        return str(self.source_detail.get('guild', {}).get('name', ''))

    @property
    def destination_guild(self):
        return str(self.destination_detail.get('guild', {}).get('name', ''))

    @property
    def reward_as_html(self):
        return markdown.parse_bounty(self.reward)

    @property
    def description_as_html(self):
        return markdown.parse_bounty(self.description)


class BountyImage(models.Model):
    bounty = models.ForeignKey(Bounty)
    updated_date = models.DateTimeField(
        auto_now=True, verbose_name=_("Latest update"), db_index=True)
    image = models.ImageField(upload_to="bounties", storage=OverwriteStorage())
    language = models.CharField(max_length=5, choices=settings.LANGUAGES)

    class Meta:
        unique_together = (('bounty', 'language',),)

    def clean(self):
        if self.language not in [l[0] for l in settings.LANGUAGES]:
            raise ValidationError(_("Locale not available."))

    def is_expired(self, expire_at=60 * 60 * 24 * 1):
        # Default is 1 day
        expire_date = self.updated_date + datetime.timedelta(seconds=expire_at)
        if expire_date < timezone.make_aware(
                datetime.datetime.now(), timezone.get_current_timezone()):
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField(verbose_name=_("Comment"))
    bounty = models.ForeignKey(Bounty)
    character_realm = models.CharField(max_length=50, verbose_name=_("Character realm"))
    character_name = models.CharField(
        max_length=50, verbose_name=_("Character name"))
    added_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date"), db_index=True)
    updated_date = models.DateTimeField(
        auto_now=True, verbose_name=_("Latest update"), db_index=True)
    is_hidden = models.BooleanField(default=False, verbose_name=_("Hidden"))
    user_ip = models.GenericIPAddressField(
        _('IP address'), unpack_ipv4=True, blank=True, null=True)

    class Meta:
        ordering = ['-added_date']
        verbose_name_plural = _('comments')

    def clean(self, as_staff=False):
        if self.bounty.comments_closed and not as_staff:
            raise ValidationError(_('Comments are closed.'))

        if self.bounty.comments_closed_by_staff and not as_staff:
            raise ValidationError(_('Comments are closed.'))

        if not is_player_character(
                self.user,
                self.character_name,
                self.character_realm, self.bounty.region) \
                and self.pk is None and not as_staff:
            raise ValidationError(_("This character is not your."))

        exists, character = is_character_exists(
            self.bounty.region, self.character_realm, self.character_name)
        if not exists and self.pk is None and not as_staff:
            raise ValidationError(
                _("Your character is below level 10 or on an inactive account."))
        if character:
            self.character_name = character.get('name')

        if not as_staff and Comment.objects.filter(
                user=self.user,
                added_date__gte=timezone.make_aware(
                    datetime.datetime.now(),
                    timezone.get_current_timezone()) - datetime.timedelta(
                        minutes=3)).exists() and self.pk is None:
            raise ValidationError(_(
                "Comment limit reached. Wait before sending a new one. "
                "Something like 3 minutes."))

        self.character_realm = self.character_realm.strip()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.bounty.save()

    def get_character_realm_display(self):
        return get_pretty_realm(self.character_realm)

    @property
    def character_thumbnail(self):
        return get_character_thumbnail(
            self.bounty.region, self.character_realm, self.character_name)

    @property
    def character_thumbnail_fallback(self):
        return get_character_thumbnail_fallback(
            self.bounty.region, self.character_realm, self.character_name)

    @property
    def character_armory(self):
        return get_character_armory(
            self.bounty.region, self.character_realm, self.character_name)

    @property
    def character_detail(self):
        return get_character(
            self.bounty.region,
            self.character_realm,
            self.character_name) or {}

    @property
    def text_as_html(self):
        return markdown.parse_comment(self.text)

    @property
    def edited(self):
        if self.updated_date - self.added_date > datetime.timedelta(seconds=1):
            return True
        return False
