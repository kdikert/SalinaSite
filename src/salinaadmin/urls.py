
from django.conf.urls import patterns, url


urlpatterns = patterns('salinaadmin.views',
     url(r'^login$', 'login', name='admin_login'),
     url(r'^logout$', 'logout', name='admin_logout'),
     
     url(r'^$', 'index', name='admin_index'),
     
     url(r'^texts/$', 'text_index', name='admin_text_index'),
     url(r'^texts/(?P<text_id>[0-9a-zA-Z_-]+)/edit$', 'text_edit', name='admin_text_edit'),
     url(r'^texts/(?P<text_id>[0-9a-zA-Z_-]+)/(?P<locale>[a-z-]+)/edit$', 'text_locale_edit', name='admin_text_locale_edit'),
     
     url(r'^productgroups/$', 'productgroup_index', name='admin_productgroup_index'),
     url(r'^productgroups/(?P<product_id>[a-z-]+)/edit$', 'productgroup_edit', name='admin_productgroup_edit'),
     
     url(r'^products/(?P<product_id>[a-z-]+)$', 'product', name='admin_product'),
     url(r'^products/add$', 'product_add', name='admin_product_add'),
     url(r'^products/(?P<product_id>[a-z-]+)/edit$', 'product_edit', name='admin_product_edit'),
)
