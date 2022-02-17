from django.db import models

# Create your models here.


class Iso_639_LanguageCode(models.Model):
    iso_639_2_code = models.CharField(max_length=3)
    iso_639_1_code = models.CharField(max_length=2, blank=True)
    english_name = models.CharField(max_length=64)
    french_name = models.CharField(max_length=64)
    german_name = models.CharField(max_length=64)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.iso_639_1_code}, '
            f'{self.iso_639_2_code}, '
            f'{self.english_name}, '
            # f'{self.french_name}, '
            # f'{self.german_name}, '
        )
