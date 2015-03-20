from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

from headhunter.bounties import views as bounties_views
from headhunter.accounts import views as accounts_views
from headhunter.battlenet import views as battlenet_views

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', accounts_views.HomeView.as_view(), name='home'),
    url(r'^logout/$', accounts_views.LogoutView.as_view(), name='logout'),
    # API
    url(r'^api/bounty',
        bounties_views.BountyListAPIView.as_view(), name='api-bounty-list'),
    url(r'^api/regions',
        battlenet_views.RegionsAPIView.as_view(), name='api-regions'),
    url(r'^api/realms',
        battlenet_views.RealmsAPIView.as_view(), name='api-realms'),
    url(r'^api/player-battletag',
        battlenet_views.PlayerBattleTagAPIView.as_view(), name='api-player-battletag'),
    url(r'^api/player-characters',
        battlenet_views.PlayerCharactersAPIView.as_view(), name='api-player-characters'),
)
