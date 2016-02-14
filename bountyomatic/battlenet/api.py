import logging
from operator import itemgetter

from django.conf import settings
from django.core.cache import cache
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from requests import Session
from requests import Request
from requests.exceptions import RequestException

from ..accounts.models import User

logger = logging.getLogger('battlenet-api')

RETRY = 5

GENDERS = {
    0: _('Male'),
    1: _('Female')
}

FACTIONS = {
    0: _('Alliance'),
    1: _('Horde'),
    2: _('Neutral'),
}

FACTIONS_RACES = {
    0: [1, 3, 4, 7, 11, 22, 25],
    1: [2, 5, 6, 8, 9, 10, 26],
    2: [24],
}

RACES = {
    1: _('Human'),
    2: _('Orc'),
    3: _('Dwarf'),
    4: _('Night Elf'),
    5: _('Undead'),
    6: _('Tauren'),
    7: _('Gnome'),
    8: _('Troll'),
    9: _('Goblin'),
    10: _('Blood Elf'),
    11: _('Draenei'),
    22: _('Worgen'),
    24: _('Pandaren'),
    25: _('Pandaren'),
    26: _('Pandaren')
}

CLASSES = {
    1: _('Warrior'),
    2: _('Paladin'),
    3: _('Hunter'),
    4: _('Rogue'),
    5: _('Priest'),
    6: _('Death Knight'),
    7: _('Shaman'),
    8: _('Mage'),
    9: _('Warlock'),
    10: _('Monk'),
    11: _('Druid')
}


def _retry(url, params={}, **kwargs):
    count = 0
    s = Session()
    params.update({'apikey': settings.SOCIAL_AUTH_BATTLENET_OAUTH2_KEY})
    while count < RETRY:
        try:
            req = Request('GET', url, params=params)
            prepped = req.prepare()
            resp = s.send(prepped, **kwargs)
            resp.json().get('status')
            logger.info("%s %s" % (prepped.url, resp.status_code))
            return resp
        except (RequestException, ValueError):
            logger.info(prepped.url)
            pass
        count += 1


def get_connected_realms(region, realm):
    for r in get_realms(region):
        if r['slug'] == realm:
            return r.get("connected_realms", tuple())
    return [realm]


def get_regions():
    from ..bounties.models import Bounty

    regions = []
    for slug, name in Bounty.REGION_CHOICES:
        regions.append({'slug': slug, 'name': str(name)})
    return regions


def refresh_player_cache(user):
    battletag, _ = get_player_battletag(user, update=True)
    user.battletag = battletag
    user.save()
    get_player_characters(user, update=True)


# CACHED
def get_realms(region, update=False):
    key = 'battlenet:realms:%s' % region
    realms = cache.get(key)
    if realms is None or update:
        realms = []
        r = _retry('https://%s.api.battle.net/wow/realm/status' % region)
        if not r:
            return realms
        realms = r.json().get('realms')
        # Dirty fix for Burning Legion
        if region == "eu":
            for realm in realms:
                if realm.get('slug') == 'internal-record-3713':
                    realm['slug'] = 'burning-legion'
                    realm['name'] = 'Burning Legion'
                    realm['connected_realms'] = ['burning-legion']
        cache.set(key, realms, timeout=settings.BATTLENET_CACHE.get('realms'))
    return realms


def is_character_exists(region, realm, character):
    r = get_character(region, realm, character)
    if r:
        return True, r
    return False, None


# CACHED
def get_character(region, realm, name, update=False, keep_latest=False):
    key = 'battlenet:character:%s:%s:%s' % (region, realm, slugify(name))
    character = cache.get(key)
    if character is None or update:
        character = {}
        r = _retry('https://%s.api.battle.net/wow/character/%s/%s?fields=guild' % (
            region, realm, name))
        if r and r.json().get('status') != 'nok':
            character = r.json()
            for faction_id, races in FACTIONS_RACES.items():
                if character.get('race') in races:
                    character.update({'faction': faction_id})
        if not character and keep_latest:
            return character
        cache.set(key, character, timeout=settings.BATTLENET_CACHE.get('character'))
    return character


def is_guild_exists(region, realm, guild):
    r = get_guild(region, realm, guild)
    if r:
        return True, r
    return False, None


# CACHED
def get_guild(region, realm, name, update=False, keep_latest=False):
    key = 'battlenet:guild:%s:%s:%s' % (region, realm, slugify(name))
    guild = cache.get(key)
    if guild is None or update:
        guild = {}
        r = _retry('https://%s.api.battle.net/wow/guild/%s/%s' % (region, realm, name))
        if r and r.json().get('status') != 'nok':
            guild = r.json()
        if not guild and keep_latest:
            return guild
        cache.set(key, guild, timeout=settings.BATTLENET_CACHE.get('guild'))
    return guild


def is_player_character(user, character, realm, regions=None):
    characters = get_player_characters(user, regions)
    for c in characters:
        if character.lower() == c['name'].lower() and \
                realm == c['normalized_realm']:
            return True
    return False


# CACHE
def get_player_characters(user, regions=None, update=False):
    if not isinstance(user, User):
        user = User.objects.get(pk=user)
    base_key = 'battlenet:player-characters:%s' % user.pk
    characters = []
    if not hasattr(user, 'social_auth') or not user.social_auth.exists():
        return characters
    if regions is None:
        regions = [r['slug'] for r in get_regions()]
    if not isinstance(regions, list):
        regions = [regions]

    for region in regions:
        key = base_key + ':' + region
        r_characters = cache.get(key)
        if r_characters is None or update:
            r_characters = []
            kwargs = {}
            base_url = 'https://%s.api.battle.net' % region
            if region == 'cn':
                kwargs = {'verify': False}
                base_url = 'https://cn.api.battlenet.com'
            r = _retry(
                '%s/wow/user/characters' % base_url,
                params={'access_token': user.social_auth.first().access_token},
                **kwargs)
            try:
                if not r or r.json().get('status') == 'nok':
                    continue
                else:
                    for character in r.json().get('characters'):
                        if character.get('level') < 10:
                            continue
                        normalized_realm = get_normalized_realm(
                            character.get('realm'), region)
                        character.update({
                            'normalized_realm': normalized_realm, 'region': region})
                        r_characters.append(character)
                    cache.set(
                        key,
                        r_characters,
                        timeout=settings.BATTLENET_CACHE.get('player_characters'))
            except ValueError:
                continue
        characters += r_characters
    return sorted(characters, key=itemgetter('realm', 'name'))


# CACHED
def get_player_battletag(user, update=False, keep_latest=False):
    if not hasattr(user, 'social_auth') or not user.social_auth.exists():
        return None, _('No social authentication attached')
    key = 'battlenet:battletag:%s' % user.pk
    battletag = cache.get(key)
    error = None
    if battletag is None or update:
        battletag = None
        r = _retry(
            'https://eu.api.battle.net/account/user',
            params={'access_token': user.social_auth.first().access_token})
        try:
            if r.json().get('status') != 'nok':
                battletag = r.json().get('battletag', battletag)
            if r.json().get('error_description'):
                error = r.json().get('error_description')
        except ValueError:
            pass
        if battletag is None and keep_latest:
            return battletag, error
        cache.set(
            key, battletag, timeout=settings.BATTLENET_CACHE.get('battletag'))
    return battletag, error


def get_normalized_realm(realm, region=None):
    if region is None:
        regions = [r['slug'] for r in get_regions()]
    else:
        regions = [region]

    for region in regions:
        realms = get_realms(region)
        for r in realms:
            if realm.lower() == r['name'].lower():
                return r['slug']
    return False


def get_pretty_realm(realm, region=None):
    if region is None:
        regions = [r['slug'] for r in get_regions()]
    else:
        regions = [region]

    for region in regions:
        realms = get_realms(region)
        for r in realms:
            if realm == r['slug']:
                return r['name']
    return False


def get_guild_thumbnail(region, realm, guild):
    detail = get_guild(region, realm, guild)
    if detail.get('side') == 0:
        return settings.STATIC_URL + "bountyomatic/img/alliance_guild.png"
    return settings.STATIC_URL + "bountyomatic/img/horde_guild.png"


def get_character_thumbnail(region, realm, character):
    base_url = "https://%s.battle.net/static-render/%s/" % (region, region)
    if region == "cn":
        base_url = "https://www.battlenet.com.cn/static-render/cn/"
    detail = get_character(region, realm, character)
    if detail:
        return base_url + detail.get(
            'thumbnail') + "?alt=wow/static/images/2d/avatar/%s-%s.jpg" % (
                detail.get('race'), detail.get('gender'))
    return get_character_thumbnail_fallback(region, realm, character)


def get_character_thumbnail_fallback(region, realm, character):
    detail = get_character(region, realm, character)
    if detail:
        return settings.STATIC_URL + "bountyomatic/img/thumbnails/%s-%s.jpg" % (
            detail.get('race'), detail.get('gender'))
    return settings.STATIC_URL + "bountyomatic/img/thumbnails/1-0.jpg"


def get_character_armory(region, realm, character):
    base_url = "http://%s.battle.net/wow/%s/character/" % (region, region)
    if region == "cn":
        base_url = "http://www.battlenet.com.cn/wow/cn/character/"
    return base_url + realm + "/" + character + "/simple"


def get_guild_armory(region, realm, guild):
    base_url = "http://%s.battle.net/wow/%s/guild/" % (region, region)
    if region == "cn":
        base_url = "http://www.battlenet.com.cn/wow/cn/guild/"
    return base_url + realm + "/" + guild + "/"


def is_token_valid(user):
    if not hasattr(user, 'social_auth') or not user.social_auth.exists():
        return False

    s = Session()
    params = {
        'apikey': settings.SOCIAL_AUTH_BATTLENET_OAUTH2_KEY,
        'access_token': user.social_auth.first().access_token}
    req = Request(
        'GET',
        'https://eu.api.battle.net/account/user',
        params=params)
    prepped = req.prepare()
    resp = s.send(prepped)
    logger.info("%s %s" % (prepped.url, resp.status_code))
    if resp.status_code == 200:
        return True
    if resp.status_code == 401:
        return False
    return True
