from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template':'public/index.html'}),
    (r'^(?P<congress>\d+)-(?P<bill_type>\w+)-(?P<bill_id>\d+)/$', 'public.views.shortcut'),
    (r'^(?P<congress>\d+)-(?P<bill_type>\w+)-(?P<bill_id>\d+)/(?P<destination>\w+)/$', 'public.views.shortcut'),
    (r'^bill/(?P<congress>\d+)-(?P<bill_type>\w+)-(?P<bill_id>\d+)/index.(?P<format>\w*)/$', 'public.views.bill'),
    (r'^bill/(?P<congress>\d+)-(?P<bill_type>\w+)-(?P<bill_id>\d+)/$', 'public.views.bill'),
    (r'^handle/$', 'public.views.handle'),
)
