from django.db import models

# Create your models here.


class Sound(models.Model):
    name = models.CharField(max_length=64, blank=True)
    link = models.URLField(blank=True)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.name}'
        )
