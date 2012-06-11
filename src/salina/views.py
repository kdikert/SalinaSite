
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def atelier_category(request):
    return render_to_response("salina/atelier_category.html", context_instance=RequestContext(request))


