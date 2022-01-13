from django.contrib import admin

# Register your models here.

from .models import Phrase
from .models import Language
from .models import Setting


admin.site.register(Phrase)
admin.site.register(Language)
admin.site.register(Setting)
