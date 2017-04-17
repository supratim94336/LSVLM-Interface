from django.conf.urls import patterns, url

from lm import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^save/$', views.save, name='save'),
    url(r'^(?P<lm_id>\d+)/$', views.lm, name='lm'),
    url(r'^edit/(?P<lm_id>\d+)/$', views.edit, name='edit'),
    url(r'^copy/(?P<lm_id>\d+)/$', views.copy, name='copy'),
    url(r'^delete/(?P<lm_id>\d+)/$', views.delete, name='delete'),
    url(r'^purge/(?P<lm_id>\d+)/$', views.purge, name='purge'),
    url(r'^save/(?P<lm_id>\d+)/$', views.save, name='save'),
    url(r'^train/(?P<lm_id>\d+)/$', views.train, name='train'),
    url(r'^arpa_file/(?P<lm_id>\d+)/$', views.arpa_file, name='arpa_file'),
    url(r'^lm_file/(?P<lm_id>\d+)/$', views.lm_file, name='lm_file'),
)
