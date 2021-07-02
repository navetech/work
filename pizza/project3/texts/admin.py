from django.contrib import admin

# Register your models here.

from .models import Phrase
from .models import TextSegment


admin.site.register(Phrase)
admin.site.register(TextSegment)
