from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from traits.models import Trait
from things.models import PickedThing


class Order(models.Model):
    dishes = models.ManyToManyField(
        PickedThing, blank=True,
        related_name='dishes_Order_related'
    )
    dishes_count = models.IntegerField(default=0, blank=True)

    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_Order_related'
    )
    date_time = models.DateTimeField(auto_now=True)

    trait = models.ForeignKey(
        Trait, blank=True, null=True, on_delete=models.CASCADE,
        related_name='trait_Order_related'
    )

    def __str__(self):
        return (
            f'{self.dishes}, {self.dishes_count}, '
            f'{self.user}, {self.date_time}, '
            f'{self.trait}'
        )


class HistoricOrder(models.Model):
    order = models.TextField(blank=True)
