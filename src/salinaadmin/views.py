
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import django.contrib.auth.views


@login_required
def index(request):
    return render_to_response("admin/index.html", context_instance=RequestContext(request))


def login(request):
    return django.contrib.auth.views.login(request, template_name='admin/login.html')


@login_required
def logout(request):
    return django.contrib.auth.views.logout(request, template_name='admin/logout.html')

