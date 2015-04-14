from bountyomatic.carotte import app


@app.task
def refresh_characters():
    from django.utils import timezone
    from django.core.cache import cache
    import datetime
    from uuid import uuid4

    from .api import get_character
    from ..bounties.models import Bounty

    already_refreshed = []
    # 24 hours timeout
    # It means that this task must not be longer that 4 hours
    # Because it will overlap with get_character timeout
    timeout = 60 * 60 * 24
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

        key = get_character.make_cache_key(
            get_character.uncached, bounty.region,
            bounty.source_realm, bounty.source_character)
        if key not in already_refreshed:
            cache.set(
                key,
                get_character(
                    bounty.region, bounty.source_realm,
                    bounty.source_character, seed=uuid4()),
                timeout=timeout)
            already_refreshed.append(key)

        key = get_character.make_cache_key(
            get_character.uncached, bounty.region,
            bounty.destination_realm, bounty.destination_character)
        if key not in already_refreshed:
            cache.set(
                key,
                get_character(
                    bounty.region, bounty.destination_realm,
                    bounty.destination_character, seed=uuid4()),
                timeout=timeout)
            already_refreshed.append(key)

        for comment in bounty.comment_set.all():
            key = get_character.make_cache_key(
                get_character.uncached, bounty.region,
                comment.character_realm, comment.character_name)
            if key not in already_refreshed:
                cache.set(
                    key,
                    get_character(
                        bounty.region, comment.character_realm,
                        comment.character_name, seed=uuid4()),
                    timeout=timeout)
                already_refreshed.append(key)
