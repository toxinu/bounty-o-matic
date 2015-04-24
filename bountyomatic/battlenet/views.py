import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.utils.translation import ugettext as _

from .api import CLASSES
from .api import FACTIONS
from .api import FACTIONS_RACES

from .api import get_realms
from .api import get_regions
from .api import get_player_battletag
from .api import get_player_characters


class PlayerCharactersAPIView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Need an authenticated user.')}),
                content_type="application/json")
        characters = get_player_characters(
            self.request.user.pk, self.request.GET.get('region', None) or None)
        for character in characters:
            klass = CLASSES.get(character.get('class'))
            if klass:
                character.update({'class_display': str(klass)})
            for faction_id, races in FACTIONS_RACES.items():
                if character.get('race') in races:
                    if FACTIONS.get(faction_id):
                        character.update(
                            {'faction_display': str(FACTIONS.get(faction_id))})
        return HttpResponse(json.dumps(characters), content_type="application/json")


class PlayerBattleTagAPIView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Need an authenticated user.')}),
                content_type="application/json")
        return HttpResponse(
            json.dumps({"battletag": get_player_battletag(self.request.user.pk)}),
            content_type="application/json")


class RealmsAPIView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        if not self.request.GET.get('region'):
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Need region parameter.')}),
                content_type="application/json")
        return HttpResponse(
            json.dumps(get_realms(self.request.GET.get('region'))),
            content_type="application/json")


class RegionsAPIView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(get_regions()), content_type="application/json")
