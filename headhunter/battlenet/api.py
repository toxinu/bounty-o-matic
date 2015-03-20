import requests
from memoize import memoize

from ..bounties.models import Bounty


def get_regions():
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


@memoize(timeout=60 * 2)
def is_character_exists(region, realm, character):
    r = requests.get('http://%s.battle.net/api/wow/character/%s/%s' % (
        region, realm, character))
    if r.json().get('status') == 'nok':
        return False, None
    return True, r.json()


@memoize(timeout=60 * 5)
def get_player_characters(user, regions=None):
    characters = []
    if not user.social_auth.exists():
        return characters
    if regions is None:
        regions = get_regions()
    if not isinstance(regions, list):
        regions = []
    for region in regions:
        kwargs = {}
        base_url = 'http://%s.battle.net/api' % region['slug']
        if region['slug'] == 'cn':
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
                characters += r.json().get('characters')
        except ValueError:
            continue
    return characters
