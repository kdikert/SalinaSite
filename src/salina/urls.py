
from django.conf.urls import patterns, url

urlpatterns = patterns('salina.views',
     url(r'^$', 'index', name='index'),
     url(r'^about$', 'about', name='about'),
     url(r'^atelier$', 'atelier', name='atelier'),
     url(r'^webshop$', 'webshop', name='webshop'),
     url(r'^contact$', 'contact', name='contact'),
)
