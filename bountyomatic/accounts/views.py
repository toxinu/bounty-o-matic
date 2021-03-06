import json

from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.generic import View
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from ..mixins import CacheMixin

from ..battlenet.api import refresh_player_cache


class HomeView(TemplateView):
    template_name = "accounts/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'user': self.request.user})
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            logout(request)
        return super().get(request, *args, **kwargs)


class RefreshBattleNetAPIView(CacheMixin, View):
    http_method_names = ['get']
    cache_timeout = 60 * 5

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponse(
                json.dumps({
                    'status': 'nok',
                    'reasons': [_('Need an authenticated user.')]}),
                content_type="application/json")
        refresh_player_cache(self.request.user)
        return HttpResponse(
            json.dumps({
                'status': 'ok',
                'reasons': [_(
                    "All data refreshed. "
                    "You'll be able to refresh again in 5 minutes.")]}),
            content_type="application/json")
