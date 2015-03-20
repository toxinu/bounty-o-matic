import json

from django.core import serializers
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError

from .models import Bounty

from ..mixins import CSRFExemptMixin


class BountyListAPIView(CSRFExemptMixin, View):
    http_method_names = ['get', 'post']
    model = Bounty

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            serializers.serialize('json', self.model.objects.all()),
            content_type='application/json')

    def post(self, request, *args, **kwargs):
        region = self.request.POST.get('region')
        source_realm = self.request.POST.get('source_realm')
        source_character = self.request.POST.get('source_character')
        destination_realm = self.request.POST.get('destination_realm')
        destination_character = self.request.POST.get('destination_character')
        reward = self.request.POST.get('reward')
        description = self.request.POST.get('description')

        bounty = Bounty(
            user=self.request.user,
            region=region,
            reward=reward,
            description=description,
            source_realm=source_realm,
            source_character=source_character,
            destination_realm=destination_realm,
            destination_character=destination_character)

        try:
            bounty.full_clean()
            bounty.save()
        except ValidationError as err:
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': str(err)}),
                content_type="application/json")

        return HttpResponse(
            serializers.serialize('json', [bounty]), content_type="application/json")
