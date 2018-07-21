from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'entry_list', views.entry_list, name='entry_list'),
	url(r'history_list', views.history_list, name='history_list'),
	url(r'update_entry', views.update_entry, name='update_entry'),
	url(r'update_history', views.update_history, name='update_history'),
	url(r'live_readout', views.live_readout, name='live_readout'),
	url(r'live_forecast', views.live_forecast, name='live_forecast'),
	url(r'live_power', views.live_power, name='live_power'),
	url(r'live_mphpool',views.live_mphpool, name='live_mphpool'),
	url(r'^history_graph/(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})$', views.history_graph, name='history_graph'),
	url(r'^live_camera', views.live_camera, name='live_camera'),
	url(r'^update_difficulty', views.update_difficulty, name='update_difficulty'),
	url(r'^display_last_difficulty', views.display_last_difficulty, name='display_last_difficulty'),
	url(r'^display_daily_profit', views.display_daily_profit, name='display_daily_profit'),
	url(r'^live_wallet', views.live_wallet, name='live_wallet'),
	url(r'^live_asicminers', views.live_asicminers, name='live_asicminers'),
	url(r'^live_gpuminers', views.live_gpuminers, name='live_gpuminers'),
]
