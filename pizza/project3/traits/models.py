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

    img = models.ImageField(
        upload_to='uploads/static/images',
        default=None, blank=True, null=True
    )

    def __str__(self):
        return (
            f'{self.short_name}, '
            f'{self.long_name}, '
            f'{self.quantity}, '
            # f'{self.img}'
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['short_name'] = to_dict(self.short_name, **settings)
        dict['long_name'] = to_dict(self.long_name, **settings)
        dict['quantity'] = to_dict(self.quantity, **settings)

        dict['img'] = {}
        if self.img:
            dict['img']['name'] = self.img.name
            dict['img']['path'] = self.img.path
            dict['img']['url'] = self.img.url
            dict['img']['height'] = self.img.height
            dict['img']['width'] = self.img.width

        return dict
