import requests
from django.conf import settings


def check(ip, response):
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': settings.RECAPTCHA_SECRET,
        'response': response,
        'remoteip': ip})

    try:
        if r.json().get('success'):
            return True
    except:
        pass
    return False
