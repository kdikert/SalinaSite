
from datetime import datetime

from django.db import models


class CMSEntry(models.Model):
    
    entry_id = models.CharField(max_length=128, db_index=True)

    description = models.TextField()

    class Meta:
        verbose_name_plural = "cms entries"
        ordering = ["entry_id"]
    
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
        return "%s (%s)" % (self.entry.entry_id, self.locale)
