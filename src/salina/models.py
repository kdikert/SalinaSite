
from datetime import datetime, timedelta
import logging

from django.conf import settings
from django.db import models
from django.db.utils import IntegrityError
from django.utils import translation
from django.db.models.signals import pre_delete


class ProductGroupManager(models.Manager):
    
    def create(self, group_id):
        cms_text_id = "product_group_%s" % group_id
        cms_text_description = "Name of product group %s" % group_id
        name_text = CMSText.objects.create(entry_id=cms_text_id,
                                           description=cms_text_description)
        try:
            product_group = super(ProductGroupManager, self).create(group_id=group_id,
                                                                    name_text=name_text)
        except:
            name_text.delete()
            raise
        
        return product_group


class ProductGroup(models.Model):
    
    group_id = models.CharField(max_length=64, db_index=True, unique=True)
    
    name_text = models.ForeignKey('CMSText', related_name='product_group_names')
    
    objects = ProductGroupManager()
    
    class Meta:
        ordering = ['group_id']
    
    def __unicode__(self):
        return "%s" % (self.group_id)

def product_group_pre_delete_handler(sender, instance, **kwargs):
    try:
        instance.name_text.delete()
    except:
        pass

pre_delete.connect(product_group_pre_delete_handler, sender=ProductGroup)


class Material(models.Model):
    
    name_text = models.ForeignKey('CMSText', related_name='material_names')
    
    class Meta:
        ordering = ['name_text__entry_id']


class ProductManager(models.Manager):
    
    def create(self, product_id, product_group):
        cms_text_id = "product_%s" % product_id
        cms_text_description = "Name of product %s" % product_id
        name_text = CMSText.objects.create(entry_id=cms_text_id,
                                           description=cms_text_description)
        try:
            product = super(ProductManager, self).create(product_id=product_id,
                                                         product_group=product_group,
                                                         name_text=name_text)
        except:
            name_text.delete()
            raise
        
        return product

    
class Product(models.Model):
    
    product_id = models.CharField(max_length=64, db_index=True, unique=True)
    product_group = models.ForeignKey(ProductGroup, related_name='products', null=False)
    
    name_text = models.ForeignKey('CMSText', related_name='product_names')
    
    materials = models.ManyToManyField(Material, through='ProductMaterial')
    
    objects = ProductManager()
    
    class Meta:
        ordering = ['product_id']

def product_pre_delete_handler(sender, instance, **kwargs):
    try:
        instance.name_text.delete()
    except:
        pass

pre_delete.connect(product_pre_delete_handler, sender=Product)


class ProductMaterial(models.Model):
    
    material = models.ForeignKey(Material)
    product = models.ForeignKey(Product)
    ordering = models.PositiveIntegerField()
    
    class Meta:
        unique_together = [('product', 'ordering')]
        ordering = ['ordering']


class ProductPart(models.Model):
    
    name_text = models.ForeignKey('CMSText')
    product = models.ForeignKey(Product, related_name='parts')
    
    time_min = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    class Meta:
        order_with_respect_to = 'product'


class ProductPartMaterial(models.Model):
    
    product_material = models.ForeignKey(Material)
    product_part = models.ForeignKey(ProductPart, related_name='materials')
    
    amount = models.CharField(max_length=64)
    
    class Meta:
        ordering = ['product_material__ordering']


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
    
    def unassigned(self):
        return self.filter(page=None)


class CMSText(models.Model):
    
    entry_id = models.CharField(max_length=128, db_index=True, unique=True)
    
    description = models.TextField()
    
    page = models.CharField(max_length=40, null=True, blank=True)
    
    objects = CMSTextManager()
    
    class Meta:
        verbose_name_plural = "cms entries"
        ordering = ["entry_id"]
    
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
    
    def get_translation_entry(self, locale):
        """Gets the appropriate CMSTranslation for the given locale. If there
        is no translation available for the given locale None is returned.
        @return: a CMSTranslation or None
        """
        try:
            return self.translations.filter(locale=locale).latest('timestamp')
        except CMSTranslation.DoesNotExist:
            return None
    
    def get_current_translation(self):
        current_language = translation.get_language()
        transl = self.get_translation_entry(current_language)
        if transl:
            return transl.text
        else:
            return self.entry_id
    
    def update_translation(self, locale, new_text, update_time=datetime.now()):
        
        if not locale in [lang[0] for lang in settings.LANGUAGES]:
            raise Exception("Locale %s not supported" % locale)
        
        try:
            transl = self.translations.filter(locale=locale).latest('timestamp')
            
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
    
    def __unicode__(self):
        return "%s (%s %s)" % (self.cms_text.entry_id, self.locale,
                               self.timestamp.strftime('%Y-%m-%d %H:%M'))

