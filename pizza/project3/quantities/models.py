from django.db import models

# Create your models here.

from currencies.models import Iso_4217_CurrencyCode


class Quantity(models.Model):
    value = models.FloatField(default=0)
    unit = models.CharField(max_length=64, blank=True)
    money = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='money_Quantity_related'
    )

    def __str__(self):
        ret = f'{self.value}'
        if self.unit:
            ret += f', {self.unit}'
        if self.money:
            ret += f', {self.money.alphabetic_code}'

        return ret
