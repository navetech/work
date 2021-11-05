from django.db import models

# Create your models here.


class Image(models.Model):
    name = models.CharField(max_length=128)
    link = models.URLField(max_length=512)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.name}'
        )
