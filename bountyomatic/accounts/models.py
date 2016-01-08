from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    battletag = models.CharField(max_length=20, null=True, blank=True)

    def clean(self):
        from ..battlenet.api import get_player_battletag

        super().clean()
        battletag, _ = get_player_battletag(self)
        if battletag:
            self.battletag = battletag

    def reset_social_auth(self):
        if hasattr(self, 'social_auth') and self.social_auth.exists():
            self.social_auth.all().delete()

    def ban(self):
        for s in Session.objects.all():
            if s.get_decoded().get('_auth_user_id') == self.id:
                s.delete()
        self.is_active = False
        self.save()
