import json

from django.core.paginator import Paginator
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError

from .models import Bounty

from ..mixins import CSRFExemptMixin


class BountySerializerMixin:
    def get_serializable_bounty_list(self, qs):
        objects = []
        for bounty in qs:
            objects.append({
                'id': bounty.pk,
                'region': bounty.region,
                'region_display': bounty.get_region_display(),
                'status': bounty.status,
                'status_display': bounty.get_status_display(),
                'source_realm': bounty.source_realm,
                'source_realm_display': bounty.get_source_realm_display(),
                'source_character': bounty.source_character,
                'destination_character': bounty.destination_character,
                'destination_realm': bounty.destination_realm,
                'destination_realm_display': bounty.get_destination_realm_display(),
                'added_date': str(bounty.added_date),
                'updated_date': str(bounty.updated_date)
            })
        return objects

    def get_serializable_bounty_detail(self, bounty):
        return {
            'id': bounty.pk,
            'region': bounty.region,
            'region_display': bounty.get_region_display(),
            'status': bounty.status,
            'status_display': bounty.get_status_display(),
            'source_realm': bounty.source_realm,
            'source_realm_display': bounty.get_source_realm_display(),
            'source_character': bounty.source_character,
            'destination_character': bounty.destination_character,
            'destination_realm': bounty.destination_realm,
            'destination_realm_display': bounty.get_destination_realm_display(),
            'added_date': str(bounty.added_date),
            'updated_date': str(bounty.updated_date)
        }


class BountyListAPIView(CSRFExemptMixin, BountySerializerMixin, View):
    http_method_names = ['get', 'post']
    model = Bounty

    def get(self, request, *args, **kwargs):
        page = self.request.GET.get('page', 1)

        p = Paginator(self.model.objects.all(), 50)
        result = {
            'count': p.count,
            'num_pages': p.num_pages,
            'page': page,
            'objects': self.get_serializable_bounty_list(p.page(page))
        }
        return HttpResponse(json.dumps(result), content_type='application/json')

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

        return HttpResponse(self.get_serializable_bounty_detail(
            bounty, content_type="application/json"))
