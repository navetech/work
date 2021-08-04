from django.contrib import admin

# Register your models here.

from .models import Setting

from .models import CountLimit

from .models import Size
from .models import Adding
from .models import Flavor
from .models import Type
from .models import Dish

from .models import OrderSize
from .models import OrderAdding
from .models import OrderFlavor
from .models import OrderType
from .models import OrderDish
from .models import Order
# from .models import HistoricOrder


admin.site.register(Setting)

admin.site.register(CountLimit)

admin.site.register(Size)
admin.site.register(Adding)
admin.site.register(Flavor)
admin.site.register(Type)
admin.site.register(Dish)

admin.site.register(OrderSize)
admin.site.register(OrderAdding)
admin.site.register(OrderFlavor)
admin.site.register(OrderType)
admin.site.register(OrderDish)
admin.site.register(Order)
# admin.site.register(HistoricOrder)
