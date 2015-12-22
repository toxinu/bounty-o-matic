from django.core.management.base import BaseCommand

from bountyomatic.battlenet.tasks import delay
from bountyomatic.battlenet.tasks import refresh_battletags


class Command(BaseCommand):
    def handle(self, *args, **options):
        delay(refresh_battletags)
