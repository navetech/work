from django.contrib import admin

# Register your models here.

from .models import QuantitySetting
from .models import Quantity


admin.site.register(QuantitySetting)
admin.site.register(Quantity)
