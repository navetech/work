from django.apps import AppConfig



from django.db.models.signals import post_save
from django.dispatch import receiver


def my_callback(sender, **kwargs):
    from .models import CountLimit

    print("Request finished!ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")

    self = kwargs['instance']
    print(self.flavors_count)
    print(self.flavors.all())

    if len(self.flavors.all()):
        if not self.flavors_count:
            self.flavors_count = CountLimit(min=2, max=3)
            self.flavors_count.save()
            self.save()
    else:
        if self.flavors_count:
            self.flavors_count = None
            self.save()


class OrdersConfig(AppConfig):
    name = 'orders'





    def ready(self):
        print('READY 1113333333333333333333333333333')


        from .models import Dish

        post_save.connect(my_callback, sender=Dish)

