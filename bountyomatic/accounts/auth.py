import requests

from social.backends.battlenet import BattleNetOAuth2

from .models import User


class BasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(BasicBackend):
    def authenticate(self, username=None, password=None):
        # If username is an email address, then try to pull it up
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            user = None
        if not user:
            # We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
        if user and user.check_password(password):
            return user


def get_username(backend, details, response, *args, **kwargs):
    access_token = response.get('access_token')
    try:
        user_response = requests.get(
            'https://eu.api.battle.net/account/user?access_token=%s' % access_token)
        username = user_response.json().get('id')
    except:
        username = None

    user = User.objects.filter(username=username)
    if user:
        return {'username': username, 'user': user[0]}
    return {'username': username}


class CustomBattleNetOAuth2(BattleNetOAuth2):
    def get_user_id(self, details, response):
        access_token = response.get('access_token')
        try:
            r = requests.get(
                'https://eu.api.battle.net/account/user?access_token=%s' % access_token)
            return r.json().get('id')
        except:
            return None
