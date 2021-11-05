from django.contrib import admin

# Register your models here.

from .models import Meaning
from .models import Transcription
from .models import Pronunciation
from .models import Spelling
from .models import Phrase


admin.site.register(Meaning)
admin.site.register(Transcription)
admin.site.register(Spelling)
admin.site.register(Pronunciation)
admin.site.register(Phrase)
