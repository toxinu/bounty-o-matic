from weasyprint import HTML

from django.conf import settings
from django.template import loader
from django.template import Context
from django.core.files.base import ContentFile

from ..models import BountyImage


def render_bounty(bounty):
    bounty_image, _ = BountyImage.objects.get_or_create(bounty=bounty)
    if bounty_image.is_expired(expire_at=1) or not bounty_image.image:
        t = loader.get_template('bounties/export.html')
        html = HTML(string=t.render(Context(
            {'bounty': bounty, 'SITE_URL': settings.SITE_URL})))
        image_content = ContentFile(html.write_png())
        image_content.name = "bounty_%s.jpg" % bounty.pk
        bounty_image.image = image_content
        bounty_image.save()
        return bounty_image.image.read()
    return bounty_image.image.read(-1)
