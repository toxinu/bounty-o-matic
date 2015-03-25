from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import View
from django.views.generic import TemplateView

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
