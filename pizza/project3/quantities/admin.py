from django.contrib import admin
from django.db.models.query_utils import Q

# Register your models here.

from .models import Quantity


admin.site.register(Quantity)

