from django.conf.urls import patterns, url

from representation import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^geocrawl$', views.GeoCrawl.as_view(), name='geocrawl'),
	url(r'^crawl$', views.crawl, name='crawl'),
	url(r'^mapview$', views.MapShow.as_view(), name='mapview'),
	url(r'^predictionview$', views.PredictionView.as_view(), name='predictionview'),
	url(r'^gridcount$', views.GridCount.as_view(), name='gridcount'),
)
