from django.contrib import admin

# Register your models here.

from .models import Quantity
from .models import Currency
from .models import Setting


admin.site.register(Quantity)
admin.site.register(Currency)
admin.site.register(Setting)
