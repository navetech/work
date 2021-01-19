from django.contrib import admin

from .models import Topping, SpecialPizza, Pizza, PizzaOrder

# Register your models here.
admin.site.register(Topping)
admin.site.register(SpecialPizza)
admin.site.register(Pizza)
admin.site.register(PizzaOrder)
