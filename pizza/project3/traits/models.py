from django.db import models

# Create your models here.

from texts.models import Phrase
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
        ret = ''
        if self.short_name:
            ret += '*****, ' + self.short_name.__str__()
        if self.long_name:
            ret += ', ' + self.long_name.__str__()
        if self.quantity:
            ret += ', ' + self.quantity.__str__()

        return ret

    def to_dict(self, dict):
        dict['id'] = self.id

        dict['short_name'] = self.short_name
        dict['long_name'] = self.long_name
        dict['quantity'] = self.quantity

        return

        return ret
