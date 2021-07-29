from django.contrib import admin

# Register your models here.

from .models import TextSetting
from .models import Phrase
from .models import Language


admin.site.register(TextSetting)
admin.site.register(Phrase)
admin.site.register(Language)
