import json

from django.core import serializers
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.http import QueryDict
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import CreateView

from .models import Bounty

from ..mixins import CSRFExemptMixin

from ..battlenet.api import get_realms
from ..battlenet.api import get_regions
from ..battlenet.api import is_player_character
from ..battlenet.api import is_character_exists
from ..battlenet.api import get_player_characters


class BountyListAPIView(CSRFExemptMixin, View):
    http_method_names = ['get', 'put']
    model = Bounty

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            serializers.serialize('json', self.model.objects.all()),
            content_type='application/json')

    def put(self, request, *args, **kwargs):
        data = QueryDict(self.request.body)
        region = data.get('region')
        source = data.get('source')
        destination_realm = data.get('destination_realm')
        destination_character = data.get('destination_character')

        if not all([region, source, destination_realm, destination_character]):
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': 'missing fields.'}),
                content_type="application/json")

        if region not in [r['slug'] for r in get_regions()]:
            return HttpResponseBadRequest(
                json.dumps({
                    'status': 'nok',
                    'reason': "This region does not exists (%s)." % region}),
                content_type="application/json")

        exists, destination = is_character_exists(
            region, destination_realm, destination_character)
        if not exists:
            return HttpResponseBadRequest(
                json.dumps({
                    'status': 'nok',
                    'reason': "Character destination does not exists."}),
                content_type="application/json")

        if not is_player_character(self.request.user, source, region):
            return HttpResponseBadRequest(
                json.dumps({
                    'status': 'nok',
                    'reason': "Character source is not your."}),
                content_type="application/json")

        bounty = Bounty.objects.create(
            amount=10,
            user=self.request.user,
            source=source,
            destination="%s-%s" % (destination_character, destination_realm))

        return HttpResponse(
            serializers.serialize('json', [bounty]), content_type="application/json")


class BountyListView(ListView):
    model = Bounty
    template_name = "bounties/list.html"


class BountyCreateView(CreateView):
    model = Bounty
    template_name = "bounties/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': {}})
        context.update({'regions': get_regions()})

        if self.request.GET.get('region'):
            context.update({'selected_region': self.request.GET.get('region')})
            context.update(
                {'player_characters': get_player_characters(
                    self.request.user, regions=self.request.GET.get('region'))})
            context.update(
                {'realms': get_realms(self.request.GET.get('region'))})
        if self.request.GET.get('source'):
            context.update({'source': self.request.GET.get('source')})
        return context

    def post(self, request, *args, **kwargs):
        region = self.request.POST.get('region')
        source = self.request.POST.get('source')
        destination_realm = self.request.POST.get('destination_realm')
        destination_character = self.request.POST.get('destination_character')

        if region not in [r['slug'] for r in get_regions()]:
            return HttpResponseBadRequest("This region does not exists (%s).")

        exists, destination = is_character_exists(
            region, destination_realm, destination_character)
        if not exists:
            return HttpResponseBadRequest("Character destination does not exists.")

        if not is_player_character(self.request.user, source, region):
            return HttpResponseBadRequest("Character source is not your.")

        Bounty.objects.create(
            amount=10,
            user=self.request.user,
            source=source,
            destination="%s-%s" % (destination_character, destination_realm))

        return redirect(reverse("bounty-list"))
