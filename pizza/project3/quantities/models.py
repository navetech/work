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
        if self.unit:
            convertion = self.convert_currency()
            if convertion:
                return convertion

        return self.value

    def convert_currency(self):
        currency = Setting.get_first_currency()

        return self.convert_currency_to(currency)

    def convert_currency_to(self, currency):
        if not currency:
            return f'{self.value:.2f} {self.unit.alphabetic_code}'
        elif currency == self.unit:
            return f'{self.value:.2f} {self.unit.alphabetic_code}'
        else:
            converted_value = c.convert(
                self.value, self.unit.alphabetic_code, currency.code.alphabetic_code
            )

            if not converted_value and converted_value != 0:
                return f'{self.value:.2f} {self.unit.alphabetic_code}'
            else:
                return f'{converted_value:.2f} {currency.code.alphabetic_code}'


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


class Setting(models.Model):
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.CASCADE,
        related_name='currency_Setting_related'
    )

    def __str__(self):
        return (
            f'{self.currency}, '
        )

    @classmethod
    def get_first_currency(cls):
        settings = cls.objects.first()
        if not settings:
            currency = Currency.objects.first()

            if currency:
                settings = cls(currency=currency)
                settings.save()
        else:
            if not settings.currency:
                currency = Currency.objects.first()

                if currency:
                    settings.currency = currency
                    settings.save()
            else:
                currency = settings.currency

        return currency
