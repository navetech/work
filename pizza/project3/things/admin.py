from django.contrib import admin

# Register your models here.


from .models import PickableThing
from .models import PickedThing


admin.site.register(PickableThing)
admin.site.register(PickedThing)
