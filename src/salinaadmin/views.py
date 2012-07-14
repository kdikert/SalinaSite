
import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils import translation
import django.forms.util

from salina.models import CMSText, CMSPage, ProductGroup, Product,\
    MaterialColumn, ProductPart, ProductPartColumn
from salina.models import _get_locale_name

from . import forms


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
def text_edit(request, text_id):
    cms_text = get_object_or_404(CMSText, entry_id=text_id)
    
    if request.method == 'POST':
        for locale_code, locale_name in settings.LANGUAGES:   #@UnusedVariable
            new_text = request.POST.get('text_%s' % locale_code, '')
            cms_text.update_translation(locale_code, new_text)
        return HttpResponseRedirect(reverse(text_index))
    else:
        translations = cms_text.get_translation_entries_per_locale_with_name()
        
        return render_to_response("salinaadmin/text_edit.html",
                                  {'text': cms_text, 'translations': translations},
                                  context_instance=RequestContext(request))


@login_required
def text_locale_edit(request, text_id, locale):
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
        
        locale_name = _get_locale_name(locale)
        
        return render_to_response("salinaadmin/text_locale_edit.html",
                                  {'text': cms_text, 'old_text': old_text,
                                   'locale_name': locale_name},
                                  context_instance=RequestContext(request))


@login_required
def productgroup_index(request):
    product_groups = ProductGroup.objects.all()
    
    
    return render_to_response("salinaadmin/productgroup_index.html",
                              {'product_groups' : product_groups},
                              context_instance=RequestContext(request))


@login_required
def productgroup_edit(request):
    return render_to_response("salinaadmin/products.html", context_instance=RequestContext(request))


@login_required
def product(request):
    return render_to_response("salinaadmin/products.html", context_instance=RequestContext(request))


@login_required
def product_add(request):
    return render_to_response("salinaadmin/products.html", context_instance=RequestContext(request))


@login_required
def product_json(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    language = translation.get_language()
    result = {}
    
    result['materials'] = [{'name' : material_column.material.name_text.get_translation(language),
                            'id' : material_column.material.material_id,
                            'pk' : material_column.material.pk}
                           for material_column in product.material_columns.all()]
    
    result['parts'] = [{'name' : product_part.name_text.get_translation(language),
                        'price' : product_part.price,
                        'time' : product_part.time_min,
                        'materials' : [{'amount' : column.amount if column is not None else '',
                                        'text' : column.text.get_translation(language) if column is not None else ''}
                                       for column in product_part.get_columns()]
                        }
                       for product_part in product.parts.all()]
    
    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    current_language = translation.get_language()
    
    material_column_formset = forms.MaterialColumnFormSet(prefix='materials')
    product_part_formset = forms.ProductPartFormSet(prefix='parts')
    
    if request.method == 'POST':
        form = forms.ProductForm(instance=product, data=request.POST)
        try:
            material_column_formset = forms.MaterialColumnFormSet(prefix='materials', data=request.POST)
            product_part_formset = forms.ProductPartFormSet(prefix='parts', data=request.POST)
        except django.forms.util.ValidationError:
            pass
            
        if form.is_valid() and material_column_formset.is_valid() and product_part_formset.is_valid():
            form.save()
            
            form.instance.parts.all().delete()
            form.instance.material_columns.all().delete()
            
            material_columns = []
            for material_form in material_column_formset.forms:
                material_column = MaterialColumn.objects.create(product=product,
                                                                material=material_form.cleaned_data['material'])
                material_columns.append(material_column)
            
            for product_part_form in product_part_formset.forms:
                product_part = ProductPart.objects.create(product=product,
                                                          time_min=product_part_form.cleaned_data['time_min'],
                                                          price=product_part_form.cleaned_data['price'])
                product_part.name_text.update_translation(current_language, product_part_form.cleaned_data['name'])
                
                for material_index, material_column in enumerate(material_columns):
                    amount = product_part_form.cleaned_data['amount-%d' % material_index]
                    text = product_part_form.cleaned_data['text-%d' % material_index]
                    
                    column = ProductPartColumn.objects.create(product_part=product_part,
                                                              material_column=material_column,
                                                              amount=amount)
                    column.text.update_translation(current_language, text)
            
            return HttpResponseRedirect(reverse(productgroup_index))
    else:
        form = forms.ProductForm(instance=product)
    
    for i, material_column_form in enumerate(material_column_formset):
        material_column_form.index = i
    
    return render_to_response("salinaadmin/product_edit.html",
                              {'form': form,
                               'material_column_formset': material_column_formset,
                               'product_part_formset': product_part_formset,
                               'product': product},
                              context_instance=RequestContext(request))

