from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from languages.models import Iso_639_LanguageCode


class TextSetting(models.Model):
    target_language = models.ForeignKey(
        Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name='target_language_TextSetting_related'
    )

    def __str__(self):
        return f'{self.target_language}'


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
#        return self.words
        return self.translate()


    def translate(self):
        setting = TextSetting.objects.first()
        if setting and setting.target_language:
            target = setting.target_language
        else:
            target = Iso_639_LanguageCode.objects.order_by('sort_number').first()

        origins = self.languages.all().order_by('sort_number')

        for origin in origins:
            if target == origin:
                return self.words

        phrases = Phrase.objects.all()
        for phrase in phrases:
            if phrase != self and target in phrase.languages.all():
                if phrase.translation_of:
                    if (
                        phrase.translation_of == self or
                        phrase.translation_of == self.translation_of
                    ):
                        return phrase.words
        
        return self.words


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


class UserLanguage(models.Model):
    language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_UserLanguage_related'
    )

    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_UserLanguage_related'
    )

    def __str__(self):
        return (
            f'{self.language}, '
            f'{self.user}, '
        )
