from django.contrib import admin

# Register your models here.

from .models import Theme
from .models import BaseWord
from .models import Image
from .models import Word
from .models import Language
from .models import TransliterationSystem
from .models import PronunciationSpelling
from .models import Pronunciation
from .models import Definition
from .models import Example
from .models import Spelling
from .models import Phrase


admin.site.register(Theme)
admin.site.register(BaseWord)
admin.site.register(Image)
admin.site.register(Word)
admin.site.register(Language)
admin.site.register(TransliterationSystem)
admin.site.register(PronunciationSpelling)
admin.site.register(Pronunciation)
admin.site.register(Definition)
admin.site.register(Example)
admin.site.register(Spelling)
admin.site.register(Phrase)
