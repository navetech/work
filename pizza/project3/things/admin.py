from django.contrib import admin

# Register your models here.


from .models import Thing
from .models import PickedThing


admin.site.register(Thing)
admin.site.register(PickedThing)
