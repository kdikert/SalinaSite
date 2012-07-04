
from django.forms.models import ModelForm, ModelChoiceField
from django.forms import CharField, IntegerField, TextInput
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from salina import models


class ProductForm(ModelForm):
    
    product_group = ModelChoiceField(models.ProductGroup.objects.all(), empty_label=None)

    class Meta:
        model = models.Product
        fields = ('product_id', 'is_displayed')


class MaterialColumnForm(ModelForm):
    
    material = ModelChoiceField(models.Material.objects.all(), empty_label=None)
    
    class Meta:
        model = models.MaterialColumn
        fields = []


MaterialColumnFormSet = formset_factory(MaterialColumnForm, extra=1)


class ProductPartForm(ModelForm):
    
    name = CharField()
    time_min = IntegerField(min_value=0,
                            label=_("minutes"),
                            widget=TextInput(attrs={'size': '3', 'maxlength' : 4}))
    price = IntegerField(min_value=0,
                         label=mark_safe('&euro;'),
                         widget=TextInput(attrs={'size': '2', 'maxlength' : 3}))
    
    class Meta:
        model = models.ProductPart
        fields = []


ProductPartFormSet = formset_factory(ProductPartForm, extra=1)
