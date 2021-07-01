from django.db import models

# Create your models here.

from traits.models import Trait


class Thing(models.Model):
    trait = models.ForeignKey(
        Trait, on_delete=models.CASCADE,
        related_name='trait_%(app_label)s_%(class)s_related'
    )

    basics = models.ManyToManyField(
        'self', blank=True,
        related_name='basics_%(app_label)s_%(class)s_related'
    )
    basics_min_count = models.IntegerField(default=0, blank=True)
    basics_max_count = models.IntegerField(default=0, blank=True)

    adds = models.ManyToManyField(
        'self', blank=True, related_name='adds_%(app_label)s_%(class)s_related'
    )
    adds_min_count = models.IntegerField(default=0, blank=True)
    adds_max_count = models.IntegerField(default=0, blank=True)

    sort_number = models.FloatField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.trait}, {self.basics}, '
            f'{self.basics_min_count}, {self.basics_max_count}, '
            f'{self.adds}, {self.adds_min_count}, {self.adds_max_count}, '
            f'{self.sort_number}'
        )


class PickableThing(Thing):
    pass


class PickedThing(Thing):
    count = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{Thing.__str__(self)}, {self.count}, {self.date_time}'
