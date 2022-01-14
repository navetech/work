from django.contrib import admin

# Register your models here.

from .models import Setting

from .models import CountLimit

from .models import Size
from .models import Adding
from .models import Flavor
from .models import Type
from .models import Dish

from .models import MenuItem


admin.site.register(Setting)

admin.site.register(CountLimit)

admin.site.register(Size)
admin.site.register(Adding)
admin.site.register(Flavor)
admin.site.register(Type)

admin.site.register(MenuItem)
