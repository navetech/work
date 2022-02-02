from django.contrib import admin

# Register your models here.

from .models import Setting

from .models import CountLimit

from .models import Size
from .models import AddingFlavorSize
from .models import AddingFlavor
from .models import AddingFlavorSet
from .models import Adding
from .models import Flavor
from .models import Type
from .models import Dish
from .models import Menu

from .models import OrderSize
from .models import OrderAddingFlavorSize
from .models import OrderAddingFlavor
from .models import OrderAdding
from .models import OrderFlavor
from .models import OrderType
from .models import OrderDish
from .models import OrderMenu
from .models import OrderItem
from .models import Order

admin.site.register(Setting)

admin.site.register(CountLimit)

admin.site.register(Size)
admin.site.register(AddingFlavorSize)
admin.site.register(AddingFlavor)
admin.site.register(AddingFlavorSet)
admin.site.register(Adding)
admin.site.register(Flavor)
admin.site.register(Type)
admin.site.register(Dish)
admin.site.register(Menu)

admin.site.register(OrderSize)
admin.site.register(OrderAddingFlavorSize)
admin.site.register(OrderAddingFlavor)
admin.site.register(OrderAdding)
admin.site.register(OrderFlavor)
admin.site.register(OrderType)
admin.site.register(OrderDish)
admin.site.register(OrderMenu)
admin.site.register(OrderItem)
admin.site.register(Order)
