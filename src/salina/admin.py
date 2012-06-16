
from django.contrib import admin

from .models import Material
from .models import ProductGroup
from .models import Product
from .models import CMSText
from .models import CMSTranslation

admin.site.register(Material)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(CMSText)
admin.site.register(CMSTranslation)

