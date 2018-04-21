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
	#url('^history_graph\/[0-9]{4}\/[0-9]{2}\/[0-9]{2}', views.history_graph, name='history_graph'),
]