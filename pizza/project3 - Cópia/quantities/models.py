from django.db import models

# Create your models here.

from currency_converter import CurrencyConverter

from currencies.models import Iso_4217_CurrencyCode

from texts.models import Phrase
from texts.models import to_dict


c = CurrencyConverter()


class Quantity(models.Model):
    value = models.FloatField(default=0, blank=True)
    unit = models.ForeignKey(
        Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='unit_Quantity_related'
    )

    def __str__(self):
        if self.unit:
            return (
                f'{self.value:.2f} '
                f'{self.unit.alphabetic_code}'
            )
        else:
            return (
                f'{self.value:.2f} '
            )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['value'] = self.value
        dict['unit'] = self.unit.alphabetic_code

        if settings and settings['currency']:
            currency = settings['currency']
        else:
            currency = None

        dict['converted'] = self.convert_currency_to(currency)

        return dict

    def convert_currency(self):
        currency = Setting.get_first_currency()

        return self.convert_currency_to(currency)

    def convert_currency_to(self, currency):
        converted = {
            'value': self.value,
            'unit': '',
        }

        if not (self.unit and self.unit.alphabetic_code):
            return converted
        else:
            converted['unit'] = self.unit.alphabetic_code

            if not (
                currency and currency.code and
                currency.code.alphabetic_code
            ):
                return converted
            elif currency.code.alphabetic_code == self.unit.alphabetic_code:
                return converted
            else:
                converted_value = c.convert(
                    self.value, self.unit.alphabetic_code,
                    currency.code.alphabetic_code
                )

                if not converted_value and converted_value != 0:
                    return converted
                else:
                    converted = {
                        'value': converted_value,
                        'unit': currency.code.alphabetic_code,
                    }
                    return converted


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
            f'{self.code.alphabetic_code}, '
            f'{self.name}'
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['code'] = self.code.alphabetic_code

        dict['name'] = to_dict(self.name, **settings)

        return dict


class Setting(models.Model):
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.CASCADE,
        related_name='currency_Setting_related'
    )

    def __str__(self):
        return (
            f'{self.currency}'
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
