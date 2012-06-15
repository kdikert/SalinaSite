
from django.contrib import admin

from .models import CMSText
from .models import CMSTranslation

admin.site.register(CMSText)
admin.site.register(CMSTranslation)

