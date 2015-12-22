import asyncio


def delay(task_method, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_method(*args, **kwargs))
    loop.close()


@asyncio.coroutine
def refresh_realms():
    from .api import get_realms
    from .api import get_regions
    for region in get_regions():
        get_realms(region.get('slug'), update=True)


@asyncio.coroutine
def refresh_battletags():
    from .api import get_player_battletag
    from ..accounts.models import User

    for user in User.objects.all():
        battletag, error = get_player_battletag(user, update=True)
        if battletag != user.battletag:
            user.battletag = battletag
            user.save()


@asyncio.coroutine
def refresh_characters():
    import time
    time.sleep(50)
    import datetime
    from django.utils import timezone

    from .api import get_character
    from ..bounties.models import Bounty

    already_refreshed = []
    # Approx. 6 month
    bounties_range = 1 * 30 * 6
    for bounty in Bounty.objects.filter(
            updated_date__gte=timezone.make_aware(
                datetime.datetime.now(),
                timezone.get_current_timezone()) - datetime.timedelta(
            days=bounties_range)).only(
                'region', 'source_character', 'source_realm',
                'destination_character', 'destination_realm').prefetch_related(
                    'comment_set'):

        key = '%s|%s|%s' % (
            bounty.region, bounty.source_realm, bounty.source_character)
        if key not in already_refreshed:
            get_character(
                bounty.region,
                bounty.source_realm,
                bounty.source_character,
                update=True, keep_latest=True)
            already_refreshed.append(key)

        key = '%s|%s|%s' % (
            bounty.region,
            bounty.destination_realm,
            bounty.destination_character)
        if key not in already_refreshed:
            get_character(
                bounty.region,
                bounty.destination_realm,
                bounty.destination_character,
                update=True, keep_latest=True)
            already_refreshed.append(key)

        for comment in bounty.comment_set.all():
            key = '%s|%s|%s' % (
                bounty.region, comment.character_realm, comment.character_name)
            if key not in already_refreshed:
                get_character(
                    bounty.region,
                    comment.character_realm,
                    comment.character_name,
                    update=True, keep_latest=True)
                already_refreshed.append(key)
