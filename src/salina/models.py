
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
import logging
from django.db.utils import IntegrityError


class ProductGroup(models.Model):
    
    name = models.CharField(max_length=40)
    slug = models.CharField(max_length=40)


class Product(models.Model):
    
    name = models.CharField(max_length=40)
    slug = models.CharField(max_length=40)
    product_group = models.ForeignKey(ProductGroup, related_name='products')


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
        return CMSEntry.objects.filter(page=self.page_id)
    
    def __unicode__(self):
        return self.description


class CMSEntryManager(models.Manager):
    
    def unassigned(self):
        return self.filter(page=None, product_group=None, product=None)


class CMSEntry(models.Model):
    
    entry_id = models.CharField(max_length=128, db_index=True)
    
    description = models.TextField()
    
    page = models.CharField(max_length=40, null=True, blank=True)
    
    product_group = models.ForeignKey(ProductGroup, related_name='texts', null=True, blank=True)
    
    product = models.ForeignKey(Product, related_name='texts', null=True, blank=True)
    
    objects = CMSEntryManager()
    
    class Meta:
        verbose_name_plural = "cms entries"
        ordering = ["entry_id"]
    
    def has_translation(self, locale):
        return self.translations.filter(locale=locale).count() > 0
    
    def get_translation_entry(self, locale):
        """Gets the appropriate CMSTranslation for the given locale. If there
        is no translation available for the given locale None is returned.
        @return: a CMSTranslation or None
        """
        try:
            return self.translations.filter(locale=locale).latest('timestamp')
        except CMSTranslation.DoesNotExist:
            return None
    
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
    
    def update_translation(self, locale, new_text):
        try:
            transl = self.translations.filter(locale=locale).latest('timestamp')
            
            treshold = timedelta(seconds=settings.SALINA_CMS_TEXT_AMEND_TRESHOLD_SECONDS)
            if datetime.now() - transl.timestamp < treshold:
                logging.debug("Amending to previous entry (%s)", transl)
                transl.text = new_text
                transl.timestamp = datetime.now()
            else:
                logging.debug("Previous entry too old (%s)", transl)
                transl = None
        except CMSTranslation.DoesNotExist:
            transl = None
            
        if not transl:
            transl = CMSTranslation(entry=self, locale=locale, text=new_text)
        
        transl.save()
    
    def __unicode__(self):
        return self.entry_id

    def save(self, *args, **kwargs):
        
        if not CMSPage.objects.get_page(self.page):
            self.page = None
        
        relationships = 0
        if self.page:
            relationships += 1
        if self.product_group:
            relationships += 1
        if self.product:
            relationships += 1
        
        if relationships > 1:
            raise IntegrityError("CMS Text can be related to only one object")
        
        return super(CMSEntry, self).save(*args, **kwargs)


class CMSTranslation(models.Model):
    
    entry = models.ForeignKey(CMSEntry, related_name='translations')
    
    locale = models.CharField(max_length=5, db_index=True)
    
    text = models.TextField()
    
    timestamp = models.DateTimeField(db_index=True, default=datetime.now)
    
    class Meta:
        unique_together = [('entry', 'locale', 'timestamp'), ]
        ordering = ['entry__entry_id', 'locale', '-timestamp']
    
    def __unicode__(self):
        return "%s (%s %s)" % (self.entry.entry_id, self.locale,
                               self.timestamp.strftime('%Y-%m-%d %H:%M'))

