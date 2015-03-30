from weasyprint import CSS
from weasyprint import HTML
from django.template import loader
from django.template import Context

from django.contrib.staticfiles import finders


def render(context):
    t = loader.get_template('bounties/export.html')
    css_path = finders.find('bountyomatic/css/export.css')
    return HTML(string=t.render(Context(context))).write_png(
        stylesheets=[CSS(filename=css_path)])
