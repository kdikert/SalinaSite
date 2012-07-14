
from django.forms.models import ModelForm, ModelChoiceField,\
    modelformset_factory
from django.forms import CharField, IntegerField, TextInput, Form
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
        fields = ('material', )


#MaterialColumnFormSet = modelformset_factory(model=models.MaterialColumn, form=MaterialColumnForm, extra=1)
MaterialColumnFormSet = formset_factory(MaterialColumnForm, extra=1)


class ProductPartForm(ModelForm):
    
    name = CharField()
    time_min = IntegerField(min_value=0,
                            label=_("minutes"),
                            widget=TextInput(attrs={'size': '3', 'maxlength' : 4}))
    price = IntegerField(min_value=0,
                         label=mark_safe('&euro;'),
                         widget=TextInput(attrs={'size': '2', 'maxlength' : 3}))
    
    def __init__(self, data=None, files=None, *args, **kwargs):
        super(ProductPartForm, self).__init__(data, files, *args, **kwargs)
        
        if data:
            try:
                number_of_columns = int(data['materials-TOTAL_FORMS'])
            except:
                number_of_columns = 0
            
            for i in range(number_of_columns):
                self.fields['amount-%d' % i] = CharField(required=False)
                self.fields['text-%d' % i] = CharField(required=False)
        
#        print data if data is not None else "Data is None"
#        print files if files is not None else "Files is None"
    
    class Meta:
        model = models.ProductPart
        fields = ['name', 'time_min', 'price']


ProductPartFormSet = formset_factory(ProductPartForm, extra=1)
