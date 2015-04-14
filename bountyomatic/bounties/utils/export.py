from weasyprint import HTML

from django.conf import settings
from django.template import loader
from django.template import Context
from django.core.files.base import ContentFile

from ..models import BountyImage


def render_bounty(bounty, language):
    bounty_image = None
    try:
        bounty_image = BountyImage.objects.get(bounty=bounty, language=language)
    except BountyImage.DoesNotExist:
        pass
    if not bounty_image or bounty_image.is_expired(expire_at=1):
        if not bounty_image:
            bounty_image = BountyImage(bounty=bounty, language=language)

        bounty_image.language = language
        t = loader.get_template('bounties/export.html')
        html = HTML(string=t.render(Context(
            {'bounty': bounty, 'SITE_URL': settings.SITE_URL})))
        image_content = ContentFile(html.write_png())
        image_content.name = "bounty_%s_%s.jpg" % (bounty.pk, language)
        bounty_image.image = image_content
        bounty_image.clean()
        bounty_image.save()
        return bounty_image.image.read()
    return bounty_image.image.read(-1)
