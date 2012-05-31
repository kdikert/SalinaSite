
from django.contrib import admin

from .models import CMSEntry
from .models import CMSTranslation

admin.site.register(CMSEntry)
admin.site.register(CMSTranslation)

