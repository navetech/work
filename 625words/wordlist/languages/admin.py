from django.contrib import admin

# Register your models here.

from .models import Iso_639_LanguageCode
from .models import TransliterationSystem


admin.site.register(Iso_639_LanguageCode)
admin.site.register(TransliterationSystem)
