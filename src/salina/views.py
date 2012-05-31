
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse


def index(request):
    return render_to_response("salina/index.html", context_instance=RequestContext(request))


def about(request):
    return render_to_response("salina/about.html", context_instance=RequestContext(request))


def atelier(request):
    return render_to_response("salina/atelier.html", context_instance=RequestContext(request))


def webshop(request):
    return render_to_response("salina/webshop.html", context_instance=RequestContext(request))


def contact(request):
    return render_to_response("salina/contact.html", context_instance=RequestContext(request))


