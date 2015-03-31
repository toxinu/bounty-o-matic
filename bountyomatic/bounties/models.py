import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .utils import markdown
from ..battlenet.api import CLASSES
from ..battlenet.api import FACTIONS
from ..battlenet.api import FACTIONS_RACES
from ..battlenet.api import get_character
from ..battlenet.api import get_pretty_realm
from ..battlenet.api import is_player_character
from ..battlenet.api import is_character_exists
from ..battlenet.api import get_character_armory
from ..battlenet.api import get_character_thumbnail


class Bounty(models.Model):
    REGION_EU = 'eu'
    REGION_US = 'us'
    REGION_KR = 'kr'
    REGION_TW = 'tw'
    REGION_CHOICES = (
        (REGION_EU, _('Europe')),
        (REGION_US, _('US')),
        (REGION_KR, _('Korea')),
        (REGION_TW, _('Taiwan')),)

    STATUS_OPEN = 1
    STATUS_CLOSE = 2
    STATUS_CANCELLED = 3
    STATUS_CHOICES = (
        (STATUS_OPEN, _('Open')),
        (STATUS_CLOSE, _('Closed')),
        (STATUS_CANCELLED, _('Cancelled')),)

    reward = models.TextField(verbose_name=_("Reward"))
    description = models.TextField(verbose_name=_("Description"))
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=STATUS_OPEN, verbose_name=_("Status"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    region = models.CharField(
        max_length=2,
        choices=REGION_CHOICES,
        default=REGION_EU,
        verbose_name=_("Region"))

    source_realm = models.CharField(max_length=50, verbose_name=_("Source realm"))
    source_character = models.CharField(
        max_length=50, verbose_name=_("Source character"))
    destination_realm = models.CharField(max_length=50, verbose_name=_("Target realm"))
    destination_character = models.CharField(
        max_length=50, verbose_name=_("Target character"))

    added_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("Latest update"))

    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'bounties'
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
        if self.source_realm == self.destination_realm:
            if self.source_character == self.destination_character:
                raise ValidationError(
                    _("Your character and target must be different."))

        exists, destination = is_character_exists(
            self.region, self.destination_realm, self.destination_character)
        if not exists and not self.pk:
            raise ValidationError(
                _("Target character does not exists or is below level 10."))

        exists, source = is_character_exists(
            self.region, self.source_realm, self.source_character)
        if not exists and not self.pk:
            raise ValidationError(
                _("Your character is below level 10 or on inactive account."))

        if not is_player_character(
                self.user,
                self.source_character,
                self.source_realm, self.region) and not self.pk:
            raise ValidationError(_("This character is not your."))

        self.reward = strip_tags(self.reward)
        self.description = strip_tags(self.description)

    def get_source_realm_display(self):
        return get_pretty_realm(self.source_realm)

    def get_destination_realm_display(self):
        return get_pretty_realm(self.destination_realm)

    @property
    def source_detail(self):
        return get_character(self.region, self.source_realm, self.source_character) or {}

    @property
    def destination_detail(self):
        return get_character(
            self.region, self.destination_realm, self.destination_character) or {}

    @property
    def source_thumbnail(self):
        return get_character_thumbnail(
            self.region, self.source_realm, self.source_character)

    @property
    def destination_thumbnail(self):
        return get_character_thumbnail(
            self.region, self.destination_realm, self.destination_character)

    @property
    def destination_armory(self):
        return get_character_armory(
            self.region, self.destination_realm, self.destination_character)

    @property
    def source_armory(self):
        return get_character_armory(
            self.region, self.source_realm, self.source_character)

    @property
    def source_faction_display(self):
        for faction_id, races in FACTIONS_RACES.items():
            if self.source_detail.get('race') in races:
                if FACTIONS.get(faction_id):
                    return str(FACTIONS.get(faction_id))

    @property
    def destination_faction_display(self):
        for faction_id, races in FACTIONS_RACES.items():
            if self.destination_detail.get('race') in races:
                if FACTIONS.get(faction_id):
                    return str(FACTIONS.get(faction_id))

    @property
    def source_class_display(self):
        klass = CLASSES.get(self.source_detail.get('class'))
        if klass:
            return str(klass)

    @property
    def destination_class_display(self):
        klass = CLASSES.get(self.destination_detail.get('class'))
        if klass:
            return str(klass)

    @property
    def reward_as_html(self):
        return markdown.parse_bounty(self.reward)

    @property
    def description_as_html(self):
        return markdown.parse_bounty(self.description)


class BountyImage(models.Model):
    bounty = models.OneToOneField(Bounty)
    updated_date = models.DateTimeField(
        auto_now=True, verbose_name=_("Latest update"), db_index=True)
    image = models.ImageField(upload_to="bounties")

    def is_expired(self, expire_at=60 * 60 * 24 * 7):
        # Default is 7 days
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
    is_hidden = models.BooleanField(default=False, verbose_name=_("Hidden"))
    user_ip = models.GenericIPAddressField(
        _('IP address'), unpack_ipv4=True, blank=True, null=True)

    class Meta:
        ordering = ['-added_date']

    def clean(self):
        if not is_player_character(
                self.user,
                self.character_name,
                self.character_realm, self.bounty.region) and not self.pk:
            raise ValidationError(_("This character is not your."))

        if Comment.objects.filter(
                user=self.user,
                added_date__gte=timezone.make_aware(
                    datetime.datetime.now(),
                    timezone.get_current_timezone()) - datetime.timedelta(
                        minutes=1)).exists():
            raise ValidationError(
                _("Comment limit reached. Wait before sending a new one."))

        self.text = strip_tags(self.text)

    def get_character_realm_display(self):
        return get_pretty_realm(self.character_realm)

    @property
    def character_thumbnail(self):
        return get_character_thumbnail(
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
