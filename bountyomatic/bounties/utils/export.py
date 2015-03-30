from weasyprint import CSS
from weasyprint import HTML

from django.template import loader
from django.template import Context
from django.contrib.staticfiles import finders

from requests_cache.core import CachedSession


def fetcher(url):
    s = CachedSession(expire_after=60 * 60 * 24 * 1)
    s.get(url)
    resp = s.get(url)
    return {
        'string': resp.content,
        'mime_type': resp.headers.get('content-type'),
        'encoding': resp.encoding}


def render_bounty(bounty):
    t = loader.get_template('bounties/export.html')
    css_path = finders.find('bountyomatic/css/export.css')

    html = HTML(string=t.render(Context({'bounty': bounty})), url_fetcher=fetcher)
    return html.write_png(stylesheets=[CSS(filename=css_path)])
