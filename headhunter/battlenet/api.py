import requests
from memoize import memoize


def get_regions():
    from ..bounties.models import Bounty

    regions = []
    for slug, name in Bounty.REGION_CHOICES:
        regions.append({'slug': slug, 'name': name})
    return regions


@memoize(timeout=60 * 30)
def get_realms(region):
    r = requests.get('http://%s.battle.net/api/wow/realm/status' % region)
    realms = []
    for realm in r.json().get('realms'):
        realms.append({'name': realm.get('name'), 'slug': realm.get('slug')})
    return realms


@memoize(timeout=60 * 5)
def is_character_exists(region, realm, character):
    r = requests.get('http://%s.battle.net/api/wow/character/%s/%s' % (
        region, realm, character))
    if r.json().get('status') == 'nok':
        return False, None
    return True, r.json()


@memoize(timeout=60 * 5)
def is_player_character(user, character, realm, regions=None):
    characters = get_player_characters(user, regions)
    for c in characters:
        if character == c['name'] and realm == c['normalized_realm']:
            return True
    return False


@memoize(timeout=60 * 5)
def get_player_characters(user, regions=None):
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
        r = requests.get(
            '%s/wow/user/characters' % base_url,
            params={'access_token': user.social_auth.first().access_token},
            **kwargs)
        try:
            if r.json().get('status') == 'nok':
                continue
            else:
                for character in r.json().get('characters'):
                    normalized_realm = get_normalized_realm(
                        character.get('realm'), region)
                    character.update({
                        'normalized_realm': normalized_realm, 'region': region})
                    characters.append(character)
        except ValueError:
            continue
    return characters


@memoize(timeout=60 * 30)
def get_player_battletag(user):
    if not user.social_auth.exists():
        return None
    r = requests.get(
        'http://eu.battle.net/api/account/user/battletag',
        params={'access_token': user.social_auth.first().access_token})
    try:
        if r.json().get('status') == 'nok':
            return None
        else:
            return r.json().get('battletag')
    except ValueError:
        return None


def get_normalized_realm(realm, region=None):
    if region is None:
        regions = [r['slug'] for r in get_regions()]
    else:
        regions = [region]

    for region in regions:
        realms = get_realms(region)
        for r in realms:
            if realm == r['name']:
                return r['slug']


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
