from django.conf.urls import patterns, url

from corpora import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^(?P<corpus_id>\d+)/$', views.corpus, name='corpus'),
    url(r'^edit/(?P<corpus_id>\d+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<corpus_id>\d+)/$', views.delete, name='delete'),
    url(r'^purge/(?P<corpus_id>\d+)/$', views.purge, name='purge'),
    url(r'^count_file/(?P<count_file_id>\d+)/$', views.count_file, name='count_file')
)
