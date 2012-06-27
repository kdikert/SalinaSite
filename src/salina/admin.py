
from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Material
from .models import ProductGroup
from .models import Product
from .models import CMSText
from .models import CMSTranslation

class CMSTextListFilter(admin.SimpleListFilter):
    title = _('included texts')
    parameter_name = 'texts'

    def lookups(self, request, model_admin):
        return (
            ('no_products', _('No products')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no_products':
            return queryset.exclude(entry_id__startswith='product_')
        # All
        return queryset

class CMSTextAdmin(admin.ModelAdmin):
    list_filter = (CMSTextListFilter, )


admin.site.register(Material)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(CMSText, CMSTextAdmin)
admin.site.register(CMSTranslation)
