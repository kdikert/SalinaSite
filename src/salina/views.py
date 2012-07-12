
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from salina.models import ProductGroup, Product


def atelier(request):
    product_groups = ProductGroup.objects.all()
    
    return render_to_response("salina/atelier.html",
                              {'product_groups' : product_groups},
                              context_instance=RequestContext(request))


def atelier_category(request, group_id):
    product_group = get_object_or_404(ProductGroup, group_id=group_id)
    products = Product.objects.filter_displayed().filter(product_group=product_group)
    product_groups = ProductGroup.objects.all()
    
    return render_to_response("salina/atelier_category.html",
                              {'product_groups' : product_groups,
                               'product_group' : product_group,
                               'products' : products},
                              context_instance=RequestContext(request))


