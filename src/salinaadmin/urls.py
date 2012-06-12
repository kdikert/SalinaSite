
from django.conf.urls import patterns, url


urlpatterns = patterns('salinaadmin.views',
     url(r'^login$', 'login', name='admin_login'),
     url(r'^logout$', 'logout', name='admin_logout'),
     
     url(r'^$', 'index', name='admin_index'),
     url(r'^texts/$', 'texts', name='admin_texts'),
     url(r'^products/$', 'products', name='admin_products'),
)
