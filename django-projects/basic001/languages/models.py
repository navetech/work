from django.db import models

# Create your models here.

class Iso_639_LanguageCode(models.Model):
    iso_639_2_code = models.CharField(max_length=3)
    iso_639_1_code = models.CharField(max_length=2, blank=True)
    english_name = models.CharField(max_length=64)
    french_name = models.CharField(max_length=64)
    german_name = models.CharField(max_length=64)

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return f"{self.iso_639_2_code}, {self.iso_639_1_code}, {self.english_name}, {self.french_name}, {self.german_name}, {self.sort_number}"

