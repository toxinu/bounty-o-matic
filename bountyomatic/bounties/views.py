import json

from django.conf import settings
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.views.generic import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Bounty
from .models import Comment
from .utils import export
from .utils import akismet
from .utils import recaptcha
from ..mixins import CSRFExemptMixin


class BountyBaseView:
    def get_filter_kwargs(self):
        filter_kwargs = {}
        region = self.request.GET.get('region', None)
        status = self.request.GET.get('status', None)
        realm = self.request.GET.get('realm', None)
        destination_character = self.request.GET.get('destination', None)
        if region:
            filter_kwargs.update({'region': region})
        if status:
            filter_kwargs.update({'status': status})
        if realm:
            filter_kwargs.update({'destination_realm': realm})
        if destination_character:
            filter_kwargs.update(
                {'destination_character__icontains': destination_character})

        if 'owned' in self.request.GET:
            filter_kwargs.update({'user': self.request.user.pk})
        else:
            filter_kwargs.update({'is_private': False})
        return filter_kwargs

    def get_serializable_comment_list(self, qs, as_datetime=False):
        objects = []
        for comment in qs:
            added_date = comment.added_date
            if not as_datetime:
                added_date = str(added_date)

            objects.append({
                'id': comment.pk,
                'user': comment.user.pk,
                'text': comment.text_as_html,
                'region': comment.bounty.region,
                'region_display': comment.bounty.get_region_display(),
                'character_realm': comment.character_realm,
                'character_realm_display': comment.get_character_realm_display(),
                'character_name': comment.character_name,
                'character_thumbnail': comment.character_thumbnail,
                'character_armory': comment.character_armory,
                'character_guild': comment.character_detail.get('guild', {}).get('name'),
                'added_date': added_date
            })
        return objects

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
                'user': bounty.user.pk,
                'region': bounty.region,
                'region_display': bounty.get_region_display(),
                'status': bounty.status,
                'status_display': bounty.get_status_display(),
                'is_private': bounty.is_private,
                'source_realm': bounty.source_realm,
                'source_realm_display': bounty.get_source_realm_display(),
                'source_armory': bounty.source_armory,
                'source_character': bounty.source_character,
                'source_guild': bounty.source_detail.get('guild', {}).get('name'),
                'destination_character': bounty.destination_character,
                'destination_realm': bounty.destination_realm,
                'destination_realm_display': bounty.get_destination_realm_display(),
                'destination_armory': bounty.destination_armory,
                'destination_faction': bounty.destination_detail.get('faction'),
                'destination_faction_display': bounty.destination_detail.get(
                    'faction_display'),
                'destination_guild': bounty.destination_detail.get(
                    'guild', {}).get('name'),
                'added_date': added_date,
                'updated_date': updated_date,
                'comments_count': bounty.comment_set.filter(is_hidden=False).count()
            })
        return objects

    def get_serializable_bounty_detail(
            self, bounty, comments_page=None, as_datetime=False):
        added_date = bounty.added_date
        updated_date = bounty.updated_date
        if not as_datetime:
            added_date = str(added_date)
            updated_date = str(updated_date)

        comments_dict = {}
        if comments_page:
            comments_paginator = Paginator(
                bounty.comment_set.filter(is_hidden=False), 20)
            comments_dict = {
                'count': comments_paginator.count,
                'num_pages': comments_paginator.num_pages,
                'page': comments_page,
                'objects': self.get_serializable_comment_list(
                    comments_paginator.page(comments_page), as_datetime=as_datetime)
            }
        return {
            'id': bounty.pk,
            'user': bounty.user.pk,
            'region': bounty.region,
            'region_display': bounty.get_region_display(),
            'status': bounty.status,
            'status_display': bounty.get_status_display(),
            'is_private': bounty.is_private,
            'source_thumbnail': bounty.source_thumbnail,
            'source_armory': bounty.source_armory,
            'source_realm': bounty.source_realm,
            'source_realm_display': bounty.get_source_realm_display(),
            'source_character': bounty.source_character,
            'source_faction': bounty.source_detail.get('faction'),
            'source_faction_display': bounty.source_faction_display,
            'source_class_display': bounty.source_class_display,
            'source_guild': bounty.source_detail.get('guild', {}).get('name'),
            'source_level': bounty.source_detail.get('level'),
            'destination_thumbnail': bounty.destination_thumbnail,
            'destination_character': bounty.destination_character,
            'destination_realm': bounty.destination_realm,
            'destination_realm_display': bounty.get_destination_realm_display(),
            'destination_armory': bounty.destination_armory,
            'destination_faction': bounty.destination_detail.get('faction'),
            'destination_faction_display': bounty.destination_faction_display,
            'destination_class_display': bounty.destination_class_display,
            'destination_guild': bounty.destination_detail.get('guild', {}).get('name'),
            'destination_level': bounty.destination_detail.get('level'),
            'winner_character': bounty.winner_character,
            'winner_realm': bounty.winner_realm,
            'winner_realm_display': bounty.get_winner_realm_display(),
            'winner_armory': bounty.winner_armory,
            'winner_faction': bounty.winner_detail.get('faction'),
            'winner_faction_display': bounty.winner_faction_display,
            'winner_class_display': bounty.winner_class_display,
            'winner_guild': bounty.winner_detail.get('guild', {}).get('name'),
            'winner_level': bounty.winner_detail.get('level'),
            'added_date': added_date,
            'updated_date': updated_date,
            'reward': bounty.reward,
            'reward_as_html': bounty.reward_as_html,
            'description': bounty.description,
            'description_as_html': bounty.description_as_html,
            'comments': comments_dict,
        }


class BountyListAPIView(BountyBaseView, CSRFExemptMixin, View):
    http_method_names = ['get', 'post']
    model = Bounty

    def get(self, request, *args, **kwargs):
        page = self.request.GET.get('page', 1)
        filter_kwargs = self.get_filter_kwargs()

        import ipdb; ipdb.set_trace()
        p = Paginator(self.model.objects.filter(**filter_kwargs), 50)
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
        is_private = self.request.POST.get('is_private')

        if is_private == "true":
            is_private = True
        else:
            is_private = False

        bounty = Bounty(
            user=self.request.user,
            region=region,
            reward=reward,
            description=description,
            source_realm=source_realm,
            source_character=source_character,
            destination_realm=destination_realm,
            destination_character=destination_character,
            is_private=is_private)

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


class BountyDetailAPIView(BountyBaseView, CSRFExemptMixin, View):
    http_method_names = ['get', 'post']
    model = Bounty
    fields = [
        'description', 'reward', 'status',
        'is_private', 'winner_character', 'winner_realm']

    def get(self, request, *args, **kwargs):
        try:
            bounty = Bounty.objects.prefetch_related('comment_set').get(
                pk=int(self.kwargs.get('bounty_id')))
        except ValueError:
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Invalid bounty.')}),
                content_type="application/json")
        except Bounty.DoesNotExist:
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Bounty does not exist.')}),
                content_type="application/json")

        comments_page = self.request.GET.get('comments_page', 1)

        return HttpResponse(json.dumps(
            self.get_serializable_bounty_detail(bounty, comments_page)),
            content_type="application/json")

    def post(self, request, *args, **kwargs):
        try:
            bounty = Bounty.objects.get(pk=int(self.kwargs.get('bounty_id')))
        except ValueError:
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Invalid bounty.')}),
                content_type="application/json")
        except Bounty.DoesNotExist:
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Bounty does not exist.')}),
                content_type="application/json")

        if bounty.user != self.request.user:
            return HttpResponseForbidden(
                json.dumps({'status': 'nok', 'reason': _('Bounty is not yours.')}),
                content_type="application/json")

        modified = False
        for field in self.fields:
            value = request.POST.get(field, None)
            if field == 'is_private':
                if value == 'true':
                    value = True
                else:
                    value = False
            elif field == 'status':
                value = int(value)
            if value is not None and value != getattr(bounty, field):
                setattr(bounty, field, value)
                modified = True
        if modified:
            try:
                bounty.clean()
                bounty.save()
            except ValidationError as err:
                return HttpResponseBadRequest(
                    json.dumps({'status': 'nok', 'reasons': err.messages}),
                    content_type="application/json")
        return HttpResponse(json.dumps(
            self.get_serializable_bounty_detail(bounty, 1)),
            content_type="application/json")


class BountyExportAPIView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        try:
            bounty = Bounty.objects.prefetch_related('comment_set').get(
                pk=int(self.kwargs.get('bounty_id')))
            return HttpResponse(
                export.render_bounty(bounty), content_type="image/png")
        except ValueError:
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Invalid bounty.')}),
                content_type="application/json")


class BountyDetailView(BountyBaseView, TemplateView):
    template_name = "bounties/detail.html"

    def get_context_data(self, bounty_id):
        context = super().get_context_data()
        comments_page = self.request.GET.get('comments_page', 1)

        try:
            bounty = Bounty.objects.get(pk=bounty_id)
            context.update({'bounty': self.get_serializable_bounty_detail(
                bounty, comments_page, as_datetime=True)})
        except Bounty.DoesNotExist:
            pass

        context.update({'RECAPTCHA_KEY': settings.RECAPTCHA_KEY})

        return context


class BountyListView(BountyBaseView, TemplateView):
    template_name = "bounties/list.html"
    model = Bounty

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            page = 1

        filter_kwargs = self.get_filter_kwargs()

        p = Paginator(self.model.objects.filter(**filter_kwargs), 50)
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


class BountyAddCommentAPIView(CSRFExemptMixin, View):
    model = Comment
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        text = self.request.POST.get('comment')
        bounty_id = self.kwargs.get('bounty_id')
        character_name = self.request.POST.get('character_name')
        character_realm = self.request.POST.get('character_realm')
        captcha = self.request.POST.get('captcha')

        try:
            bounty = Bounty.objects.get(pk=int(bounty_id))
        except (Bounty.DoesNotExist, ValueError):
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reason': _('Bounty does not exist.')}),
                content_type="application/json")

        comment = Comment(
            user=self.request.user,
            text=text,
            bounty=bounty,
            character_name=character_name,
            character_realm=character_realm,
            user_ip=self.request.META.get('REMOTE_ADDR'))
        try:
            comment.clean()
            if not recaptcha.check(self.request.META.get('REMOTE_ADDR'), captcha):
                return HttpResponseBadRequest(
                    json.dumps({
                        'status': 'nok',
                        'reason': _('Bad captcha')}),
                    content_type="application/json")
            if akismet.verify_key():
                if akismet.comment_check(
                        request.META.get('REMOTE_ADDR', ''),
                        request.META.get('HTTP_USER_AGENT', ''),
                        referrer=request.META.get('HTTP_REFERRER', ''),
                        comment_content=text):
                    return HttpResponseBadRequest(
                        json.dumps({
                            'status': 'nok',
                            'reason': _('Your comment is a spam.')}),
                        content_type="application/json")
            comment.save()
        except ValidationError as err:
            return HttpResponseBadRequest(
                json.dumps({'status': 'nok', 'reasons': err.messages}),
                content_type="application/json")

        return HttpResponse(
            json.dumps({"status": "ok", "reason": _("Comment added.")}),
            content_type="application/json")
