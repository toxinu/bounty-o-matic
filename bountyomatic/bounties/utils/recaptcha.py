import requests
from django.conf import settings


def check(ip, response):
    count = 0
    while count < 3:
        try:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'secret': settings.RECAPTCHA_SECRET,
                'response': response,
                'remoteip': ip})
            if r.json().get('success'):
                return True
            return False
        except:
            pass
        count += 1
    return False
