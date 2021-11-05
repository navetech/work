from django.db import models

# Create your models here.


class Iso_639_LanguageCode(models.Model):
    iso_639_2_code = models.CharField(max_length=3)
    iso_639_1_code = models.CharField(max_length=2, blank=True)
    english_name = models.CharField(max_length=128, blank=True)
    french_name = models.CharField(max_length=128, blank=True)
    german_name = models.CharField(max_length=128, blank=True)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.iso_639_2_code}, '
            f'{self.iso_639_1_code}, '
            f'{self.english_name}'
        )


class TransliterationScript(models.Model):
    name = models.CharField(max_length=128)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.name}'
        )


class TranscriptionSystem(models.Model):
    name = models.CharField(max_length=128)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.name}'
        )


class PronunciationForm(models.Model):
    name = models.CharField(max_length=128)

    sort_number = models.FloatField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{self.name}'
        )
