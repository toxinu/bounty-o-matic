from django.views.generic import View
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse

from .models import Bounty


class BountyDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        bounty_id = self.kwargs.get('bounty_id')
        if bounty_id > 136:
            return HttpResponseNotFound()
        bounty = Bounty.objects.filter(pk=bounty_id).only('slug')
        if not bounty:
            return HttpResponseNotFound()
        return redirect(reverse('bounty-detail', kwargs={'bounty_slug': bounty[0].slug}))


class BountySignatureAPIView(View):
    def dispatch(self, request, *args, **kwargs):
        bounty_id = self.kwargs.get('bounty_id')
        if bounty_id > 136:
            return HttpResponseNotFound()
        bounty = Bounty.objects.filter(pk=bounty_id).only('slug')
        if not bounty:
            return HttpResponseNotFound()
        return redirect(reverse('bounty-detail', kwargs={'bounty_slug': bounty[0].slug}))


class CommentEditView(View):
    def dispatch(self, request, *args, **kwargs):
        bounty_id = self.kwargs.get('bounty_id')
        comment_id = self.kwargs.get('comment_id')
        if bounty_id > 136:
            return HttpResponseNotFound()
        bounty = Bounty.objects.filter(pk=bounty_id).only('slug')
        if not bounty:
            return HttpResponseNotFound()
        return redirect(reverse(
            'comment-detail',
            kwargs={'bounty_slug': bounty[0].slug, 'comment_id': comment_id}))
