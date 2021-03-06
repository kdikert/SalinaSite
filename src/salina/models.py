
from datetime import datetime, timedelta
import logging
import re
import markdown

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import IntegrityError
from django.db.models.signals import pre_save, post_delete
from django.db.models.aggregates import Sum
from django.utils import translation
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe


def _check_valid_id(id_text):
    if not re.match('^[a-z0-9\-]+$', id_text):
        raise ValidationError(_("The id field can only contain lower case letters a-z, numbers and dashes"))


class Material(models.Model):
    
    material_id = models.CharField(max_length=64, db_index=True, unique=True)
    
    name_text = models.ForeignKey('CMSText', related_name='material_names', editable=False)
    
    class Meta:
        ordering = ['material_id']
    
    def clean(self, exclude=None):
        # Note: only called by model forms...
        _check_valid_id(self.material_id)
    
    def __unicode__(self):
        return "%s" % (self.name_text.get_current_translation())

def material_pre_save_handler(sender, instance, **kwargs):
    if instance.name_text_id is None:
        cms_text_id = "material-%s" % instance.material_id
        cms_text_description = "Material %s" % instance.material_id
        name_text = CMSText.objects.create(entry_id=cms_text_id,
                                           description=cms_text_description,
                                           short=True)
        instance.name_text = name_text

pre_save.connect(material_pre_save_handler, sender=Material)

def material_post_delete_handler(sender, instance, **kwargs):
    try:
        instance.name_text.delete()
    except:
        pass

post_delete.connect(material_post_delete_handler, sender=Material)


class ProductGroup(models.Model):
    
    group_id = models.CharField(max_length=64, db_index=True, unique=True)
    
    name_text = models.ForeignKey('CMSText', related_name='product_group_names', editable=False)
    
    description_text = models.ForeignKey('CMSText', related_name='product_group_descriptions', editable=False)
    
    class Meta:
        ordering = ['group_id']
    
    def clean(self, exclude=None):
        _check_valid_id(self.group_id)
    
    def __unicode__(self):
        return "%s" % (self.name_text.get_current_translation())

def product_group_pre_save_handler(sender, instance, **kwargs):
    if instance.name_text_id is None:
        cms_text_id = "productgroup-%s" % instance.group_id
        cms_text_description = "Product group %s" % instance.group_id
        name_text = CMSText.objects.create(entry_id=cms_text_id,
                                           description=cms_text_description,
                                           short=True)
        instance.name_text = name_text
    
    if instance.description_text_id is None:
        cms_text_id = "productgroup-%s-description" % instance.group_id
        cms_text_description = "Product group %s description" % instance.group_id
        description_text = CMSText.objects.create(entry_id=cms_text_id,
                                           description=cms_text_description,
                                           short=False)
        instance.description_text = description_text

pre_save.connect(product_group_pre_save_handler, sender=ProductGroup)

def product_group_post_delete_handler(sender, instance, **kwargs):
    try:
        instance.name_text.delete()
    except:
        pass
    try:
        instance.description_text.delete()
    except:
        pass

post_delete.connect(product_group_post_delete_handler, sender=ProductGroup)


class ProductManager(models.Manager):
    
    def filter_displayed(self):
        return self.filter(is_displayed=True)


class Product(models.Model):
    
    product_id = models.CharField(max_length=64, db_index=True, unique=True)
    product_group = models.ForeignKey(ProductGroup, related_name='products', null=False)
    is_displayed = models.BooleanField(verbose_name=ugettext_lazy('Is displayed in list'))
    
    name_text = models.ForeignKey('CMSText', related_name='product_names', editable=False)
    
    objects = ProductManager()
    
    class Meta:
        ordering = ['product_id']
    
    def clean(self, exclude=None):
        _check_valid_id(self.product_id)
    
    def get_total_time(self):
        result = self.parts.all().aggregate(total=Sum('time_min'))
        if result['total'] is None:
            return 0
        else:
            return result['total']
    
    def get_total_price(self):
        result = self.parts.all().aggregate(total=Sum('price'))
        if result['total'] is None:
            return 0
        else:
            return result['total']
    
    def __unicode__(self):
        return "%s" % (self.product_id, )

def product_pre_save_handler(sender, instance, **kwargs):
    if instance.name_text_id is None:
        cms_text_id = "product-%s" % instance.product_id
        cms_text_description = "Product %s" % instance.product_id
        name_text = CMSText.objects.create(entry_id=cms_text_id,
                                           description=cms_text_description,
                                           short=True)
        instance.name_text = name_text

pre_save.connect(product_pre_save_handler, sender=Product)

def product_post_delete_handler(sender, instance, **kwargs):
    try:
        instance.name_text.delete()
    except:
        pass

post_delete.connect(product_post_delete_handler, sender=Product)


class MaterialColumn(models.Model):
    
    material = models.ForeignKey(Material)
    product = models.ForeignKey(Product, related_name='material_columns')
    
    class Meta:
        order_with_respect_to = 'product'
        ordering = ['_order']
    
    def get_text_translated(self):
        return self.material.name_text.get_current_translation()
    
    def __unicode__(self):
        return "%s %s" % (self.product, self.material)


class ProductPart(models.Model):
    
    name_text = models.ForeignKey('CMSText')
    product = models.ForeignKey(Product, related_name='parts')
    
    time_min = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    class Meta:
        order_with_respect_to = 'product'
    
    def get_columns(self):
        result = []
        for material_column in self.product.material_columns.all():
            try:
                column = self.columns.get(material_column=material_column)
            except ProductPartColumn.DoesNotExist:
                column = None
            result.append(column)
        return result
    
    def __unicode__(self):
        part_index = self._order + 1
        return "%s part %d" % (self.product, part_index)

def product_part_pre_save_handler(sender, instance, **kwargs):
    if instance.name_text_id is None:
        product = instance.product
        cms_text_id = CMSText.objects.get_free_id('productpart')
        cms_text_description = "Product %s part" % (product.product_id)
        name_text = CMSText.objects.create(entry_id=cms_text_id,
                                           description=cms_text_description,
                                           short=True)
        instance.name_text = name_text

pre_save.connect(product_part_pre_save_handler, sender=ProductPart)

def product_part_post_delete_handler(sender, instance, **kwargs):
    try:
        instance.name_text.delete()
    except:
        pass

post_delete.connect(product_part_post_delete_handler, sender=ProductPart)


class ProductPartColumn(models.Model):
    
    material_column = models.ForeignKey(MaterialColumn)
    product_part = models.ForeignKey(ProductPart, related_name='columns')
    
    amount = models.CharField(max_length=64)
    text = models.ForeignKey('CMSText')
    
    class Meta:
        ordering = ['material_column___order']
    
    def get_text_translated(self):
        return "%s %s" % (self.amount, self.text.get_current_translation())
    
    def __unicode__(self):
        return "%s %s" % (self.product_part, self.material_column.material)

def product_part_column_pre_save_handler(sender, instance, **kwargs):
    if instance.text_id is None:
        product = instance.product_part.product
        cms_text_id = CMSText.objects.get_free_id('productpartcolumn')
        cms_text_description = "Product %s part column" % (product.product_id)
        text = CMSText.objects.create(entry_id=cms_text_id,
                                      description=cms_text_description,
                                      short=True)
        instance.text = text

pre_save.connect(product_part_column_pre_save_handler, sender=ProductPartColumn)

def product_part_column_post_delete_handler(sender, instance, **kwargs):
    try:
        instance.text.delete()
    except:
        pass

post_delete.connect(product_part_column_post_delete_handler, sender=ProductPartColumn)


KNOWN_PAGES = (
   ('index', 'Home page'),
   ('about', 'Who we are page'),
   ('atelier', 'Atelier page'),
   ('webshop', 'Webshop page'),
   ('contact', 'Contact info page'),
)

class CMSPageManager(object):
    
    _pages = None
    
    def _populate(self):
        if CMSPageManager._pages is None:
            CMSPageManager._pages = dict((page_id, CMSPage(page_id, description))
                                         for page_id, description in KNOWN_PAGES)
    
    def get_page(self, page_id):
        self._populate()
        try:
            return CMSPageManager._pages[page_id]
        except KeyError:
            return None
    
    def all_pages(self):
        self._populate()
        return list(CMSPageManager._pages.values())


class CMSPage(object):
    
    objects = CMSPageManager()
    
    def __init__(self, page_id, description):
        self.page_id = page_id
        self.description = description
    
    def get_texts(self):
        return CMSText.objects.filter(page=self.page_id)
    
    def __unicode__(self):
        return self.description


class CMSTextManager(models.Manager):
    
    def get_free_id(self, prefix):
        index = 0
        
        existing_entries = self.filter(entry_id__startswith=prefix).order_by('-entry_id')
        if existing_entries.count():
            match = re.match('.*-([0-9]+)$', existing_entries[0].entry_id)
            if match:
                index = int(match.group(1)) + 1
        
        return "%s-%d" % (prefix, index)
    
    def unassigned(self):
        return self.filter(page=None)


def _get_locale_name(locale_code):
    for code, name in settings.LANGUAGES:
        if code == locale_code:
            return name
    return _("Unknown language")


class CMSText(models.Model):
    
    entry_id = models.CharField(max_length=128, db_index=True, unique=True)
    
    description = models.TextField()
    
    short = models.BooleanField(default=False)
    
    page = models.CharField(max_length=40, null=True, blank=True)
    
    objects = CMSTextManager()
    
    class Meta:
        verbose_name_plural = "cms entries"
        ordering = ["entry_id"]
    
    def clean(self, exclude=None):
        _check_valid_id(self.entry_id)
    
    def has_translation(self, locale):
        return self.translations.filter(locale=locale).count() > 0
    
    def get_translation_entries_per_locale(self):
        """Lists all available locales and the corresponding CMSTranslations.
        @return: a list of tuples: (locale_code, CMSTranslation or None)
        """
        result = []
        for locale_code, locale_name in settings.LANGUAGES:   #@UnusedVariable
            try:
                transl = self.translations.filter(locale=locale_code).defer('text').latest('timestamp')
            except CMSTranslation.DoesNotExist:
                transl = None
            result.append((locale_code, transl))
        
        return result
    
    def get_translation_entries_per_locale_with_name(self):
        translations = self.get_translation_entries_per_locale()
        return [(locale, _get_locale_name(locale), transl) for locale, transl in translations]

    def get_translation_entry(self, locale):
        """Gets the appropriate CMSTranslation for the given locale. If there
        is no translation available for the given locale None is returned.
        @return: a CMSTranslation or None
        """
        try:
            return self.translations.filter(locale=locale).latest('timestamp')
        except CMSTranslation.DoesNotExist:
            return None
    
    def get_translation(self, locale):
        result = self.get_translation_entry(locale)
        if result:
            return result.text
        else:
            return None
    
    def get_current_translation_entry(self):
        current_language = translation.get_language()
        return self.get_translation_entry(current_language)
    
    def get_current_translation(self):
        transl = self.get_current_translation_entry()
        if transl:
            return transl.text
        else:
            return self.entry_id
    
    def update_translation(self, locale, new_text, update_time=datetime.now()):
        
        if not locale in [lang[0] for lang in settings.LANGUAGES]:
            raise Exception("Locale %s not supported" % locale)
        
        if self.short:
            if new_text is None:
                self.delete_translation(locale)
            else:
                self.overwrite_translation(locale, new_text, update_time)
            return
        
        try:
            transl = self.translations.filter(locale=locale).latest('timestamp')
            
            if transl.text == new_text:
                return
            
            treshold = timedelta(seconds=settings.SALINA_CMS_TEXT_AMEND_TRESHOLD_SECONDS)
            if update_time - transl.timestamp < treshold:
                logging.debug("Amending to previous entry (%s)", transl)
                transl.text = new_text
                transl.timestamp = update_time
            else:
                logging.debug("Previous entry too old (%s)", transl)
                transl = None
        except CMSTranslation.DoesNotExist:
            transl = None
        
        if not transl:
            transl = CMSTranslation(cms_text=self, locale=locale, text=new_text, timestamp=update_time)
        
        transl.save()
    
    def overwrite_translation(self, locale, new_text, update_time=datetime.now()):
        
        if not locale in [lang[0] for lang in settings.LANGUAGES]:
            raise Exception("Locale %s not supported" % locale)
        
        self.translations.filter(locale=locale).delete()
        CMSTranslation.objects.create(cms_text=self, locale=locale,
                                      text=new_text, timestamp=update_time)
    
    def delete_translation(self, locale):
        self.translations.filter(locale=locale).delete()
    
    def __unicode__(self):
        return self.entry_id

    def save(self, *args, **kwargs):
        
        if not CMSPage.objects.get_page(self.page):
            self.page = None
        
        relationships = 0
        if self.page:
            relationships += 1
        
        if relationships > 1:
            raise IntegrityError("CMS Text can be related to only one object")
        
        return super(CMSText, self).save(*args, **kwargs)


class CMSTranslation(models.Model):
    
    cms_text = models.ForeignKey(CMSText, related_name='translations')
    
    locale = models.CharField(max_length=5, db_index=True)
    
    text = models.TextField()
    
    timestamp = models.DateTimeField(db_index=True, default=datetime.now)
    
    class Meta:
        unique_together = [('cms_text', 'locale', 'timestamp'), ]
        ordering = ['cms_text__entry_id', 'locale', '-timestamp']
    
    def get_markup(self, escape_content=False):
        value = force_unicode(self.text)
        
        if escape_content:
            value = escape(value)
        
        value = markdown.markdown(value)
        return mark_safe(value)
    
    def __unicode__(self):
        return "%s (%s %s)" % (self.cms_text.entry_id, self.locale,
                               self.timestamp.strftime('%Y-%m-%d %H:%M'))

