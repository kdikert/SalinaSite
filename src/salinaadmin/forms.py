
from django.forms.models import ModelForm, ModelChoiceField

from salina import models


class ProductForm(ModelForm):
    
    product_group = ModelChoiceField(models.ProductGroup.objects.all(), empty_label=None)

    class Meta:
        model = models.Product
        fields = ('product_id', )


