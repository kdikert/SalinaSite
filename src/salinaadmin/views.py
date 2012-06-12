
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(index))
    
    if request.GET.get(auth.REDIRECT_FIELD_NAME) == reverse(logout):
        return HttpResponseRedirect(reverse(login))
    
    return django.contrib.auth.views.login(request, template_name='admin/login.html')


@login_required
def logout(request):
    return django.contrib.auth.views.logout(request, template_name='admin/logout.html')


@login_required
def index(request):
    return render_to_response("admin/index.html", context_instance=RequestContext(request))


@login_required
def texts(request):
    return render_to_response("admin/texts.html", context_instance=RequestContext(request))


@login_required
def products(request):
    return render_to_response("admin/products.html", context_instance=RequestContext(request))
