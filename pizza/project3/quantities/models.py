from django.db import models

# Create your models here.

from currencies.models import Iso_4217_CurrencyCode


class Quantity(models.Model):
    value = models.FloatField(default=0)
    unit = models.CharField(max_length=64, blank=True)
    money = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='money_quantity_related'
    )

    def __str__(self):
        return f'{self.value}, {self.unit}, {self.money}'
