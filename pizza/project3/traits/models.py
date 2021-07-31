from django.db import models

# Create your models here.

from texts.models import Phrase
from texts.models import to_dict

from quantities.models import Quantity


class Trait(models.Model):
    short_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='short_name_Trait_related'
    )

    long_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='long_name_Trait_related'
    )

    quantity = models.ForeignKey(
        Quantity, blank=True, null=True, on_delete=models.CASCADE,
        related_name='quantity_Trait_related'
    )

    def __str__(self):
        return (
            f'{self.short_name}, '
            f'{self.long_name}, '
            f'{self.quantity}, '
        )

    def to_dict(self, dict, **settings):
        dict['id'] = self.id

        to_dict(self.short_name, dict, key='short_name', **settings)
        to_dict(self.long_name, dict, key='long_name', **settings)
        to_dict(self.quantity, dict, key='quantity', **settings)

        return
