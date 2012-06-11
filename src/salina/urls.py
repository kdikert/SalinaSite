
from django.conf.urls import patterns, url

from django.views.generic import TemplateView


urlpatterns = patterns('salina.views',

     url(r'^$', TemplateView.as_view(template_name="salina/index.html"), name='index'),
     url(r'^about$', TemplateView.as_view(template_name="salina/about.html"), name='about'),
     
     url(r'^atelier$', TemplateView.as_view(template_name="salina/atelier.html"), name='atelier'),
     url(r'^atelier/(?P<category_slug>[0-9a-zA-Z\d_-]+)/?$', 'atelier_category', name='atelier_category'),
     
     url(r'^webshop$', TemplateView.as_view(template_name="salina/webshop.html"), name='webshop'),
     url(r'^contact$', TemplateView.as_view(template_name="salina/contact.html"), name='contact'),
)
