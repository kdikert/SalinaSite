
from django.conf.urls import patterns, url

urlpatterns = patterns('salina.views',
     url(r'^$', 'index', name='index'),
)
