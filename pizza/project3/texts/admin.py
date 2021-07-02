from django.contrib import admin

# Register your models here.

from .models import PhraseSetting
from .models import Phrase
from .models import TextSegment


admin.site.register(PhraseSetting)
admin.site.register(Phrase)
admin.site.register(TextSegment)
