from django.contrib import admin

from .models import Size
from .models import Topping, SpecialPizza, PizzaType, PizzaFlavor, Pizza

# Register your models here.
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(SpecialPizza)
admin.site.register(PizzaType)
admin.site.register(PizzaFlavor)
admin.site.register(Pizza)
