import logging
from operator import itemgetter

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from requests import Session
from requests import Request
from requests.exceptions import RequestException

from memoize import memoize
from memoize import delete_memoized

from ..accounts.models import User

logger = logging.getLogger('battlenet-api')

RETRY = 2

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
            logger.info(prepped.url)
            resp = s.send(prepped, **kwargs)
            resp.json().get('status')
            return resp
        except (RequestException, ValueError):
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
    delete_memoized(get_player_battletag, user.pk)
    get_player_battletag(user.pk)
    delete_memoized(get_player_characters, user.pk)
    get_player_characters(user.pk)


# 5 days
@memoize(timeout=60 * 60 * 24 * 5)
def get_realms(region):
    realms = []
    r = _retry('http://%s.battle.net/api/wow/realm/status' % region)
    if not r:
        return realms
    return r.json().get('realms')


def is_character_exists(region, realm, character):
    r = get_character(region, realm, character)
    if r:
        return True, r
    return False, None


# 1 hour
@memoize(timeout=60 * 60 * 1)
def get_character(region, realm, character):
    r = _retry('http://%s.battle.net/api/wow/character/%s/%s?fields=guild' % (
        region, realm, character))
    if not r or r.json().get('status') == 'nok':
        return {}
    result = r.json()
    for faction_id, races in FACTIONS_RACES.items():
        if result.get('race') in races:
            result.update({'faction': faction_id})
    return result


def is_player_character(user, character, realm, regions=None):
    characters = get_player_characters(user, regions)
    for c in characters:
        if character.lower() == c['name'].lower() and \
                realm == c['normalized_realm']:
            return True
    return False


# 1 day
@memoize(timeout=60 * 60 * 24 * 1)
def get_player_characters(user, regions=None):
    if not isinstance(user, User):
        user = User.objects.get(pk=user)
    characters = []
    if not hasattr(user, 'social_auth') or not user.social_auth.exists():
        return characters
    if regions is None:
        regions = [r['slug'] for r in get_regions()]
    if not isinstance(regions, list):
        regions = [regions]
    for region in regions:
        kwargs = {}
        base_url = 'http://%s.battle.net/api' % region
        if region == 'cn':
            kwargs = {'verify': False}
            base_url = 'http://www.battlenet.com.cn/api'
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
                    characters.append(character)
        except ValueError:
            continue
    return sorted(characters, key=itemgetter('realm', 'name'))


# 30 days
@memoize(timeout=60 * 60 * 24 * 30)
def get_player_battletag(user):
    if not isinstance(user, User):
        user = User.objects.get(pk=user)
    if not hasattr(user, 'social_auth') or not user.social_auth.exists():
        return False
    r = _retry(
        'http://eu.battle.net/api/account/user/battletag',
        params={'access_token': user.social_auth.first().access_token})
    try:
        if not r or r.json().get('status') == 'nok':
            return False
        else:
            return r.json().get('battletag')
    except ValueError:
        return False


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


def get_character_thumbnail(region, realm, character):
    base_url = "https://%s.battle.net/static-render/%s/" % (region, region)
    if region == "cn":
        base_url = "https://www.battlenet.com.cn/static-render/cn/"
    detail = get_character(region, realm, character)
    if detail:
        return base_url + detail.get(
            'thumbnail') + "?alt=wow/static/images/2d/avatar/%s-%s.jpg" % (
                detail.get('race'), detail.get('gender'))
    return "https://%s.battle.net/wow/static/images/2d/avatar/3-0.jpg" % region


def get_character_armory(region, realm, character):
    base_url = "http://%s.battle.net/wow/%s/character/" % (region, region)
    if region == "cn":
        base_url = "http://www.battlenet.com.cn/wow/cn/character/"
    return base_url + realm + "/" + character + "/simple"
