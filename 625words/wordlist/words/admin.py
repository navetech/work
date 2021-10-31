from django.contrib import admin

# Register your models here.

from .models import Thema
from .models import Group
from .models import Word


admin.site.register(Thema)
admin.site.register(Group)
admin.site.register(Word)
