
from django.conf.urls import patterns, url


urlpatterns = patterns('salinaadmin.views',
     url(r'^login$', 'login', name='admin_login'),
     url(r'^logout$', 'logout', name='admin_logout'),
     
     url(r'^$', 'index', name='admin_index'),
     
     url(r'^texts/$', 'text_index', name='admin_text_index'),
     url(r'^texts/(?P<text_id>[0-9a-z\_\-]+)/edit$', 'text_edit', name='admin_text_edit'),
     url(r'^texts/(?P<text_id>[0-9a-z\_\-]+)/(?P<locale>[a-z-]+)/edit$', 'text_locale_edit', name='admin_text_locale_edit'),
     
     url(r'^productgroups/$', 'productgroup_index', name='admin_productgroup_index'),
     url(r'^productgroups/(?P<product_id>[0-9a-z\_\-]+)/edit$', 'productgroup_edit', name='admin_productgroup_edit'),
     
     url(r'^products/add$', 'product_add', name='admin_product_add'),
     url(r'^products/(?P<product_id>[0-9a-z\_\-]+)$', 'product', name='admin_product'),
     url(r'^products/(?P<product_id>[0-9a-z\_\-]+).json$', 'product_json', name='admin_product_json'),
     url(r'^products/(?P<product_id>[0-9a-z\_\-]+)/edit$', 'product_edit', name='admin_product_edit'),
)
