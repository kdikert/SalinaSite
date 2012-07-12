
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from salina.models import ProductGroup, Product
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def atelier(request):
    
    referrer = request.META.get('HTTP_REFERER', '')
    match = re.match('^([a-z]+\://[^/]+)?(/.*)$', referrer)
    
    if match:
        path = match.group(2)
        atelier_path = reverse('atelier')
        if path.startswith(atelier_path) and path != atelier_path:
            return HttpResponseRedirect(referrer)
    
    product_group = ProductGroup.objects.all()[0]
    return HttpResponseRedirect(reverse('atelier_group', args=[product_group.group_id]))


def atelier_group(request, group_id):
    product_group = get_object_or_404(ProductGroup, group_id=group_id)
    products = Product.objects.filter_displayed().filter(product_group=product_group)
    product_groups = ProductGroup.objects.all()
    
    return render_to_response("salina/atelier_category.html",
                              {'product_groups' : product_groups,
                               'product_group' : product_group,
                               'products' : products},
                              context_instance=RequestContext(request))


