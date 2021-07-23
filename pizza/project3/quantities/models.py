from django.db import models

# Create your models here.

from currencies.models import Iso_4217_CurrencyCode
from currency_converter import CurrencyConverter


c = CurrencyConverter()


class QuantitySetting(models.Model):
    target_currency = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='target_currency_QuantitySetting_related'
    )

    def __str__(self):
        return f'{self.target_currency}'


class Quantity(models.Model):
    value = models.FloatField(default=0, blank=True)
    unit = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='unit_Quantity_related'
    )

    def __str__(self):
        ret = f'{self.value:.2f}'
        if self.unit:
            ret += f' {self.unit.alphabetic_code}'

            convertion = self.convert_currency()
            if convertion:
                ret += ' = ' + convertion

        return ret


    def convert_currency(self):
        setting = QuantitySetting.objects.first()
        if setting and setting.target_currency:
            target = setting.target_currency
        else:
            target = Iso_4217_CurrencyCode.objects.filter(alphabetic_code='USD').first()

        if not target:
            return 'No Target Currency'

        if target == self.unit:
            return ''

        converted_value = c.convert(self.value, self.unit.alphabetic_code, target.alphabetic_code)

        if not converted_value and converted_value != 0:
            return 'Currency Convertion Failed'
        
        return f'{converted_value:.2f} {target.alphabetic_code}'
