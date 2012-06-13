
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
import logging


class CMSEntry(models.Model):
    
    entry_id = models.CharField(max_length=128, db_index=True)

    description = models.TextField()

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
