
from django.conf.urls import patterns, url


urlpatterns = patterns('salinaadmin.views',
     url(r'^login$', 'login', name='admin_login'),
     url(r'^logout$', 'logout', name='admin_logout'),
     
     url(r'^$', 'index', name='admin_index'),
     
     url(r'^texts/$', 'text_index', name='admin_text_index'),
     url(r'^texts/(?P<text_id>[0-9a-zA-Z_-]+)/edit$', 'text_edit', name='admin_text_edit'),
     url(r'^texts/(?P<text_id>[0-9a-zA-Z_-]+)/(?P<locale>[a-z-]+)/edit$', 'text_locale_edit', name='admin_text_locale_edit'),
     
     url(r'^products/$', 'products', name='admin_products'),
)
