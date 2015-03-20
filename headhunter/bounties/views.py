from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.http import HttpResponseBadRequest

from django.views.generic import ListView
from django.views.generic import CreateView

from .models import Bounty

from ..battlenet.api import get_realms
from ..battlenet.api import get_regions
from ..battlenet.api import is_player_character
from ..battlenet.api import is_character_exists
from ..battlenet.api import get_player_characters


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
