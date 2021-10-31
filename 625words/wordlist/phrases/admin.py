from django.contrib import admin

# Register your models here.

from .models import SpellingLanguage
from .models import Spelling
from .models import Pronunciation
from .models import Meaning
from .models import Phrase


admin.site.register(SpellingLanguage)
admin.site.register(Spelling)
admin.site.register(Pronunciation)
admin.site.register(Meaning)
admin.site.register(Phrase)
