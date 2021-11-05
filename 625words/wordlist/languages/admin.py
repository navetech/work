from django.contrib import admin

# Register your models here.

from .models import Iso_639_LanguageCode
from .models import TransliterationScript
from .models import TranscriptionSystem
from .models import PronunciationForm

admin.site.register(Iso_639_LanguageCode)
admin.site.register(TransliterationScript)
admin.site.register(TranscriptionSystem)
admin.site.register(PronunciationForm)
