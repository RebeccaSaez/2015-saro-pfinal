from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from prebeca.feeds import UserFeed, AllFeed

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout', "prebeca.views.logout_view"),
    url(r'^login', "prebeca.views.login"),
    url(r'^(?P<user>.*)/rss$', UserFeed()),
    url(r'^rss$', AllFeed()),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_URL2}),
    url(r'^templated-linear/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_URL2}),
    url(r'^$', "prebeca.views.root"),
    url(r'^todas$', "prebeca.views.all"),
    url(r'^ayuda$', "prebeca.views.help"),
    url(r'^incluir/(.*)$', "prebeca.views.add"),
    url(r'^eliminar/(.*)$', "prebeca.views.remove"),
    url(r'^actualizar$', "prebeca.views.refresh"),
    url(r'^actividad/(.*)$', "prebeca.views.activity"),
    url(r'^(.*)$', "prebeca.views.user")
)
