from django.db import models

# Create your models here.


class Iso_4217_CurrencyCode(models.Model):
    entity = models.CharField(max_length=64)
    currency = models.CharField(max_length=64)
    alphabetic_code = models.CharField(max_length=3, blank=True)
    numeric_code = models.DecimalField(
        max_digits=3, decimal_places=0, blank=True, null=True
    )
    minor_unit = models.IntegerField(default=2, blank=True)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            # f'{self.entity}, '
            f'{self.alphabetic_code}, '
            f'{self.currency}, '
            # f'{self.numeric_code}, '
            # f'{self.minor_unit}, '
        )
