from django.db import models

# Create your models here.

from currency_converter import CurrencyConverter

from currencies.models import Iso_4217_CurrencyCode
from texts.models import Phrase


c = CurrencyConverter()


class Quantity(models.Model):
    value = models.FloatField(default=0, blank=True)
    unit = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='unit_Quantity_related'
    )

    def __str__(self):
        ret = ''

        if self.unit:
            convertion = self.convert_currency()
            if convertion:
                ret = convertion

        return ret


    def convert_currency(self):
        settings = QuantitySetting.objects.first()
        if settings:
            if settings.user_currency:
                currency = settings.user_currency.code
            elif settings.admin_currency:
                currency = settings.admin_currency
            else:
                currency = Iso_4217_CurrencyCode.objects.filter(alphabetic_code='USD').first()
        else:
            currency = Iso_4217_CurrencyCode.objects.filter(alphabetic_code='USD').first()

        return self.convert_currency_to(currency)


    def convert_currency_to(self, currency):
        if not currency:
            return 'No Target Currency'
        elif currency == self.unit:
            return f'{self.value:.2f} {self.unit.alphabetic_code}'
        else:
            converted_value = c.convert(
                self.value, self.unit.alphabetic_code, currency.alphabetic_code
            )

            if not converted_value and converted_value != 0:
                return 'Currency Convertion Failed'
            else:
                return f'{converted_value:.2f} {currency.alphabetic_code}'


class Currency(models.Model):
    code = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='code_Currency_related'
    )

    name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='name_Currency_related'
    )

    def __str__(self):
        return (
            f'{self.code}, '
            f'{self.name}, '
        )


class QuantitySetting(models.Model):
    admin_currency = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='admin_currency_QuantitySetting_related'
    )

    user_currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_currency_QuantitySetting_related'
    )


    def __str__(self):
        return (
            f'{self.admin_currency}, '
            f'{self.user_currency}, '
        )
