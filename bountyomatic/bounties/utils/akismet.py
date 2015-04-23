from django.conf import settings
import requests

USERAGENT = ""
AKISMET_URL = "https://rest.akismet.com"
AKISMET_KEY = settings.AKISMET_KEY
AKISMET_KEY_URL = "https://%s.rest.akismet.com" % AKISMET_KEY


class AkismetError(Exception):
    def __init__(self, response, status_code):
        self.response = response
        self.status_code = status_code

    def __str__(self):
        return repr(self.response)


def __post(url, data):
    count = 0
    while count < 3:
        try:
            r = requests.post(url, data=data)
            return r.text, r.status_code
        except:
            pass
        count += 1


def verify_key():
    r, status_code = __post(
        AKISMET_URL + '/1.1/verify-key',
        {'key': AKISMET_KEY, 'blog': settings.SITE_URL})

    if r == "valid":
        return True
    elif r == "invalid":
        return False
    else:
        raise AkismetError(r, status_code)


def comment_check(user_ip, user_agent, **other):
    """Submit a comment to find out whether Akismet thinks that it's spam.
    Required parameters:
        user_ip: IP address of the being which submitted the comment.
        user_agent: User agent reported by said being.
    Suggested "other" keys: "permalink", "referrer", "comment_type", "comment_author",
    "comment_author_email", "comment_author_url", "comment_content", and any other HTTP
    headers sent from the client.
    More detail on what should be submitted is available at:
    http://akismet.com/development/api/

    Returns True if spam, False if ham.  Throws an AkismetError if the server says
    anything unexpected.
    """

    data = {'blog': settings.SITE_URL, 'user_ip': user_ip, 'user_agent': user_agent}
    data.update(other)
    r, status_code = __post(
        AKISMET_KEY_URL + "/1.1/comment-check", data)

    if r == "true":
        return True
    elif r == "false":
        return False
    else:
        raise AkismetError(r, status_code)


def submit_spam(user_ip, user_agent, **other):
    """Report a false negative to Akismet.
    Same arguments as comment_check.
    Doesn't return anything.  Throws an AkismetError if the server says anything.
    """
    data = {'blog': settings.SITE_URL, 'user_ip': user_ip, 'user_agent': user_agent}
    data.update(other)
    r, status_code = __post(
        AKISMET_KEY_URL + "/1.1/submit-spam", data)
    if status_code != 200 or r:
        raise AkismetError(r, status_code)


def submit_ham(user_ip, user_agent, **other):
    """Report a false positive to Akismet.
    Same arguments as comment_check.
    Doesn't return anything.  Throws an AkismetError if the server says anything.
    """
    data = {'blog': settings.SITE_URL, 'user_ip': user_ip, 'user_agent': user_agent}
    data.update(other)
    r, status_code = __post(
        AKISMET_KEY_URL + "/1.1/submit-ham", data)
    if status_code != 200 or r:
        raise AkismetError(r, status_code)
