from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from headhunter.bounties import views as bounties_views
from headhunter.accounts import views as accounts_views
from headhunter.battlenet import views as battlenet_views

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', accounts_views.HomeView.as_view(), name='home'),
    url(r'^logout/$', accounts_views.LogoutView.as_view(), name='logout'),
    url(r'^bounty/$',
        bounties_views.BountyListView.as_view(), name='bounty-list'),
    url(r'^bounty/add$',
        TemplateView.as_view(template_name="bounties/add.html"), name='bounty-add'),
    url(r'^bounty/(?P<bounty_id>\d+)$',
        bounties_views.BountyDetailView.as_view(), name='bounty-detail'),
    # API
    url(r'^api/bounty/(?P<bounty_id>\d+)/comment',
        bounties_views.BountyAddCommentAPIView.as_view(), name='api-bounty-comment'),
    url(r'^api/bounty/(?P<bounty_id>\d+)',
        bounties_views.BountyDetailAPIView.as_view(), name='api-bounty-detail'),
    url(r'^api/bounty',
        bounties_views.BountyListAPIView.as_view(), name='api-bounty-list'),
    url(r'^api/regions',
        battlenet_views.RegionsAPIView.as_view(), name='api-regions'),
    url(r'^api/realms',
        battlenet_views.RealmsAPIView.as_view(), name='api-realms'),
    url(r'^api/player-refresh',
        accounts_views.RefreshBattleNetAPIView.as_view(), name='api-refresh'),
    url(r'^api/player-battletag',
        battlenet_views.PlayerBattleTagAPIView.as_view(), name='api-player-battletag'),
    url(r'^api/player-characters',
        battlenet_views.PlayerCharactersAPIView.as_view(), name='api-player-characters'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
