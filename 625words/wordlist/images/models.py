from django.db import models

# Create your models here.


class Image(models.Model):
    link = models.URLField(blank=True)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.link}'
        )
