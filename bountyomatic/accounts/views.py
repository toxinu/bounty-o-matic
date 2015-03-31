import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import View
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from ..mixins import CacheMixin

from ..battlenet.api import refresh_player_cache
from ..battlenet.api import get_player_battletag


class LogoutView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class HomeView(TemplateView):
    template_name = "accounts/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'user': self.request.user})
        return context

    def get(self, request, *args, **kwargs):
        if not get_player_battletag(self.request.user):
            logout(request)
        return super().get(request, *args, **kwargs)


class RefreshBattleNetAPIView(CacheMixin, View):
    http_method_names = ['get']
    cache_timeout = 60 * 5

    def get(self, request, *args, **kwargs):
        refresh_player_cache(self.request.user)
        return HttpResponse(
            json.dumps({
                'status': 'ok',
                'reason': _(
                    "All data refreshed. "
                    "You'll be able to refresh again in 5 minutes.")}),
            content_type="application/json")
