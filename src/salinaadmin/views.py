
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from salina.models import CMSText, CMSPage


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(index))
    
    if request.GET.get(auth.REDIRECT_FIELD_NAME) == reverse(logout):
        return HttpResponseRedirect(reverse(login))
    
    return django.contrib.auth.views.login(request, template_name='salinaadmin/login.html')


@login_required
def logout(request):
    return django.contrib.auth.views.logout(request, template_name='salinaadmin/logout.html')


@login_required
def index(request):
    return render_to_response("salinaadmin/index.html", context_instance=RequestContext(request))


@login_required
def text_index(request):
    pages = CMSPage.objects.all_pages()
    unassigned_texts = list(CMSText.objects.unassigned())
    locales = settings.LANGUAGES
    
    return render_to_response("salinaadmin/text_index.html",
                              {'pages': pages,
                               'unassigned_texts': unassigned_texts,
                               'locales': locales},
                              context_instance=RequestContext(request))


@login_required
def text_edit(request, text_id, locale):
    cms_text = get_object_or_404(CMSText, entry_id=text_id)
    
    if not locale in map(lambda(locale): locale[0], settings.LANGUAGES):
        raise Http404()
    
    if request.method == 'POST':
        new_text = request.POST.get('text', '')
        cms_text.update_translation(locale, new_text)
        return HttpResponseRedirect(reverse(text_index))
    else:
        transl = cms_text.get_translation_entry(locale)
        if transl:
            old_text = transl.text
        else:
            old_text = ""
        
        locale_name = ""
        for locale_code, locale_name in settings.LANGUAGES:
            if locale_code == locale:
                break
        
        return render_to_response("salinaadmin/text_edit.html",
                                  {'text': cms_text, 'old_text': old_text,
                                   'locale_name': locale_name},
                                  context_instance=RequestContext(request))


@login_required
def products(request):
    return render_to_response("salinaadmin/products.html", context_instance=RequestContext(request))
