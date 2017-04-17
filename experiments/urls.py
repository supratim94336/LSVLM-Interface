from django.conf.urls import patterns, url
from experiments import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^run$', views.run, name='run'),
    url(r'experimentset/(?P<experiment_id>\d+)', views.experiment_set, name='experiment_set'),
    url(r'experiment/(?P<experiment_id>\d+)', views.experiment, name='experiment'),
    url(r'^delete/(?P<experiment_id>\d+)/$', views.delete, name='delete'),
    url(r'^purge/(?P<experiment_id>\d+)/$', views.purge, name='purge'),
    url(r'^results_file/(?P<experiment_id>[A-Za-z0-9]+)$', views.results_file, name='results_file'),
    url(r'^concordance_click/(?P<row_num>\d+)', views.concordance_click, name='concordance_click')
)
