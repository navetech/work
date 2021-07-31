from django.db import models

# Create your models here.

from languages.models import Iso_639_LanguageCode


class Phrase(models.Model):
    words = models.CharField(max_length=256, blank=True)

    languages = models.ManyToManyField(
        Iso_639_LanguageCode, blank=True,
        related_name='languages_Phrase_related'
    )

    translation_of = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE,
        related_name='translation_of_Phrase_related'
    )


    def __str__(self):
        return self.translate()


    def translate_to(self, language):
        if not language:
            return self.words

        origins = self.languages.all().order_by('sort_number')
        for origin in origins:
            if language.code == origin:
                return self.words

        phrases = Phrase.objects.all()
        for phrase in phrases:
            if phrase != self and phrase.translation_of:
                if (
                    phrase.translation_of == self or
                    phrase.translation_of == self.translation_of
                ):
                    if language.code in phrase.languages.all():
                        return phrase.words
        
        return self.words


    def translate(self):
        language = Setting.get_first_language()

        return self.translate_to(language)


class Language(models.Model):
    code = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='code_Language_related'
    )

    name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='name_Language_related'
    )


    def __str__(self):
        return (
            f'{self.code}, '
            f'{self.name}, '
        )


class Setting(models.Model):
    language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_Setting_related'
    )


    def __str__(self):
        return (
            f'{self.language}, '
        )


    @classmethod
    def get_first_language(cls):
        settings = cls.objects.first()
        if not settings:
            language = Language.objects.first()

            if language:
                settings = cls(language=language)
                settings.save()
        else:
            if not settings.language:
                language = Language.objects.first()

                if language:
                    settings.language = language
                    settings.save()
            else:
                language = settings.language

        return language
