from django.contrib import admin


from .models import Size, SizeAndPrice
from .models import Dish, DishTypeOrAdding, TypeOrAddingFlavor, FoodFlavor, Food
from .models import OrderStatus, Order, FoodOrder

# Register your models here.
admin.site.register(Size)
admin.site.register(SizeAndPrice)
admin.site.register(Dish)
admin.site.register(DishTypeOrAdding)
admin.site.register(TypeOrAddingFlavor)
admin.site.register(FoodFlavor)
admin.site.register(Food)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(FoodOrder)
