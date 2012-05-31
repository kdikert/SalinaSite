
from django.db import models


class CMSText(models.Model):
    
    text_id = models.CharField(max_length=128, db_index=True)
    
    locale = models.CharField(max_length=5, db_index=True)
    
    text = models.TextField()
    
    timestamp = models.DateTimeField(db_index=True)
    
    class Meta:
        unique_together = [('text_id', 'locale', 'timestamp'), ]
        ordering = ["-timestamp"]
