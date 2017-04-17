from django.conf.urls import patterns, include, url
from django.contrib import admin
from lsvlminterface import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lsvlminterface.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^static/', include(static.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/static'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^corpora/', include('corpora.urls', namespace="corpora")),
    url(r'^lm/', include('lm.urls', namespace="lm")),
    url(r'^experiments/', include('experiments.urls', namespace="experiments")),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^new_user/$', views.new_user, name="new_user"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^$', views.index, name="index")
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
