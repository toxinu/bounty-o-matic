import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.utils.translation import ugettext as _

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
        return HttpResponse(
            json.dumps(get_player_characters(
                self.request.user,
                self.request.GET.get('region', None))),
            content_type="application/json")


class PlayerBattleTagAPIView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Need an authenticated user.')}),
                content_type="application/json")
        return HttpResponse(
            json.dumps({"battletag": get_player_battletag(self.request.user)}),
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
