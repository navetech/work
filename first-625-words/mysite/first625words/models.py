from django.db import models

# Create your models here.


class Theme(models.Model):
    name = models.CharField(max_length=256)

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return (
            f'{self.name}'
            +  ', ' +
            f'{self.sort_number}'
        )


class BaseWord(models.Model):
    text = models.CharField(max_length=256)

    theme = models.ForeignKey(
        Theme, blank=True, null=True, on_delete=models.CASCADE,
        related_name='theme_BaseWord_related'
    )

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return (
            f'{self.text}'
            +  ', ' +
            f'{self.theme.name}'
            +  ', ' +
            f'{self.sort_number}'
        )


class Image(models.Model):
    link = models.URLField(max_length=1024)

    def __str__(self):
        return (
            f'{self.link}'
        )


class Word(models.Model):
    base_word = models.ForeignKey(
        BaseWord, blank=True, null=True, on_delete=models.CASCADE,
        related_name='base_word_Word_related'
    )

    grouping = models.CharField(max_length=512, default='')

    grouping_key = models.CharField(max_length=512, default='')

    images = models.ManyToManyField(
        Image, blank=True,
        related_name='images_Word_related'
    )

    def __str__(self):
        return (
            f'{self.base_word}'
            +  ', ' +
            f'{self.grouping}'
            +  ', ' +
            f'{self.grouping_key}'
        )


class TransliterationSystem(models.Model):
    name = models.CharField(max_length=256)


class PronunciationSpelling(models.Model):
    text = models.TextField()

    system = models.ForeignKey(
        TransliterationSystem, blank=True, null=True, on_delete=models.CASCADE,
        related_name='system_PronunciationSpelling_related'
    )


class Pronunciation(models.Model):
    sound = models.URLField(max_length=1024)

    spellings = models.ManyToManyField(
        PronunciationSpelling, blank=True,
        related_name='spellings_Pronunciation_related'
    )


class Spelling(models.Model):
    text = models.TextField()

    pronunciation = models.ForeignKey(
        Pronunciation, blank=True, null=True, on_delete=models.CASCADE,
        related_name='pronunciation_Spelling_related'
    )


class Language(models.Model):
    name = models.CharField(max_length=256)


class PhraseDefinition(models.Model):
    text = models.TextField()

    language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_PhraseDefinition_related'
    )


class PhraseExample(models.Model):
    text = models.TextField()

    credits = models.TextField()


class Phrase(models.Model):
    word = models.ForeignKey(
        Word, blank=True, null=True, on_delete=models.CASCADE,
        related_name='word_Phrase_related'
    )

    language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_Phrase_related'
    )

    spellings = models.ManyToManyField(
        Spelling, blank=True,
        related_name='spellings_Phrase_related'
    )

    definitions = models.ManyToManyField(
        PhraseDefinition, blank=True,
        related_name='definitions_Phrase_related'
    )

    examples = models.ManyToManyField(
        PhraseExample, blank=True,
        related_name='examples_Phrase_related'
    )
