from django.views.generic import ListView
from django.views.generic import CreateView

from .models import Bounty

from ..battlenet.api import get_regions


class BountyListView(ListView):
    model = Bounty
    template_name = "bounties/list.html"


class BountyCreateView(CreateView):
    model = Bounty
    template_name = "bounties/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'regions': get_regions()})
        return context
