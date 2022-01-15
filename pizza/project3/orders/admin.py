from django.contrib import admin

# Register your models here.

from .models import Setting

from .models import CountLimit

from .models import Size
from .models import AddingFlavor
from .models import AddingFlavorSet
from .models import Adding
from .models import Flavor
from .models import Type
from .models import Dish
from .models import Menu


admin.site.register(Setting)

admin.site.register(CountLimit)

admin.site.register(Size)
admin.site.register(AddingFlavor)
admin.site.register(AddingFlavorSet)
admin.site.register(Adding)
admin.site.register(Flavor)
admin.site.register(Type)
admin.site.register(Dish)
admin.site.register(Menu)
