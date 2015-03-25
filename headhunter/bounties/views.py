import json

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.views.generic import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError

from .models import Bounty

from ..mixins import CSRFExemptMixin


class BountySerializerMixin:
    def get_serializable_bounty_list(self, qs, as_datetime=False):
        objects = []
        for bounty in qs:
            added_date = bounty.added_date
            updated_date = bounty.updated_date
            if not as_datetime:
                added_date = str(added_date)
                updated_date = str(updated_date)

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
                'added_date': added_date,
                'updated_date': updated_date
            })
        return objects

    def get_serializable_bounty_detail(self, bounty, as_datetime=False):
        added_date = bounty.added_date
        updated_date = bounty.updated_date
        if not as_datetime:
            added_date = str(added_date)
            updated_date = str(updated_date)

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
            'added_date': added_date,
            'updated_date': updated_date,
            'reward': bounty.reward,
            'description': bounty.description
        }


class BountyListAPIView(BountySerializerMixin, CSRFExemptMixin, View):
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
                json.dumps({'status': 'nok', 'reasons': err.messages}),
                content_type="application/json")

        return HttpResponse(
            json.dumps(self.get_serializable_bounty_detail(bounty)),
            content_type="application/json")


class BountyDetailView(BountySerializerMixin, TemplateView):
    template_name = "bounties/detail.html"

    def get_context_data(self, bounty_id):
        context = super().get_context_data()

        try:
            bounty = Bounty.objects.get(pk=bounty_id)
            context.update({'bounty': self.get_serializable_bounty_detail(
                bounty, as_datetime=True)})
        except Bounty.DoesNotExist:
            pass

        return context


class BountyListView(BountySerializerMixin, TemplateView):
    template_name = "bounties/list.html"
    model = Bounty

    def get_context_data(self):
        context = super().get_context_data()

        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            page = 1

        p = Paginator(self.model.objects.all(), 50)
        try:
            bounties = self.get_serializable_bounty_list(p.page(page), as_datetime=True)
        except EmptyPage:
            bounties = []

        context.update({
            'count': p.count,
            'num_pages': p.num_pages,
            'page': page,
            'bounties': bounties
        })
        if page > 1:
            context.update({
                'has_previous': True,
                'previous_page_number': page - 1})
        if page < p.num_pages:
            context.update({
                'has_next': True,
                'next_page_number': page + 1})

        return context
