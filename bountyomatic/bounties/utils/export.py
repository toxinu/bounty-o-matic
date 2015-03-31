from weasyprint import CSS
from weasyprint import HTML

from django.template import loader
from django.template import Context
from django.contrib.staticfiles import finders
from django.core.files.base import ContentFile

from ..models import BountyImage


def render_bounty(bounty):
    bounty_image, _ = BountyImage.objects.get_or_create(bounty=bounty)
    if bounty_image.is_expired() or not bounty_image.image:
        t = loader.get_template('bounties/export.html')
        css_path = finders.find('bountyomatic/css/export.css')
        html = HTML(string=t.render(Context({'bounty': bounty})))
        raw_image = html.write_png(stylesheets=[CSS(filename=css_path)])
        image_content = ContentFile(raw_image)
        image_content.name = "bounty_%s.jpg" % bounty.pk
        bounty_image.image = image_content
        bounty_image.save()
        return raw_image
    return bounty_image.image.read(-1)
