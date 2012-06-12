
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from salina.models import CMSEntry
from salina.models import CMSTranslation


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
def text_index(request):
    locales = settings.LANGUAGES
    texts = list(CMSEntry.objects.all())
    return render_to_response("admin/text_index.html",
                              {'texts': texts, 'locales': locales},
                              context_instance=RequestContext(request))


@login_required
def text_edit(request, text_id, locale):
    text = get_object_or_404(CMSEntry, entry_id=text_id)
    
    transl = text.get_translation_entry(locale)
    if transl:
        old_text = transl.text
    else:
        old_text = ""
    
    locale_name = ""
    for locale_code, locale_name in settings.LANGUAGES:
        if locale_code == locale:
            break
    
    return render_to_response("admin/text_edit.html",
                              {'text': text, 'old_text': old_text,
                               'locale_name': locale_name},
                              context_instance=RequestContext(request))


@login_required
def products(request):
    return render_to_response("admin/products.html", context_instance=RequestContext(request))