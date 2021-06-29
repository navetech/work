from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Iso_639_LanguageCode(models.Model):
    iso_639_2_code = models.CharField(max_length=3)
    iso_639_1_code = models.CharField(max_length=2, blank=True)
    english_name = models.CharField(max_length=64)
    french_name = models.CharField(max_length=64)
    german_name = models.CharField(max_length=64)

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return f"{self.iso_639_2_code}, {self.iso_639_1_code}, {self.english_name}, {self.french_name}, {self.german_name}, {self.sort_number}"


class Text(models.Model):
    words = models.CharField(max_length=256, blank=True)
    language = models.ForeignKey(Iso_639_LanguageCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name="language_texts")

    basics = models.ManyToManyField('self', blank=True, related_name="basics_texts")

    def __str__(self):
        return f"{self.words}, {self.language}, {self.basics}"


class Iso_4217_CurrencyCode(models.Model):
    entity = models.CharField(max_length=64)
    currency = models.CharField(max_length=64)
    alphabetic_code = models.CharField(max_length=3, blank=True)
    numeric_code = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    minor_unit = models.IntegerField(default= 2, blank=True)

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return f"{self.entity}, {self.currency}, {self.alphabetic_code}, {self.nuneric_code}, {self.minor_unit}, {self.sort_number}"


class Quantity(models.Model):
    value = models.FloatField(default=0)
    unit = models.CharField(max_length=64, blank=True)
    money = models.ForeignKey(Iso_4217_CurrencyCode, blank=True, null=True, on_delete=models.CASCADE,
        related_name="currency_quantities")

    def __str__(self):
        return f"{self.value}, {self.unit}, {self.currency}"


class Trait(models.Model):
    name = models.ForeignKey(Text, blank=True, null=True, on_delete=models.CASCADE,
        related_name="name_traits")
    quantity = models.ForeignKey(Quantity, blank=True, null=True, on_delete=models.CASCADE,
        related_name="quantity_traits")

    texts = models.ManyToManyField(Text, blank=True, related_name="texts_traits")

    def __str__(self):
        return f"{self.name}, {self.quantity}, {self.texts}"


class CountLimit(models.Model):
    min = models.IntegerField(default=0)
    max = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.min}, {self.max}"


class PickableArticle(models.Model):
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE,
        related_name="trait_pickablearticles")

    basics = models.ManyToManyField('self', blank=True, related_name="basics_pickablearticles")
    basics_count = models.ForeignKey(CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name="basicscount_pickablearticles")

    adds = models.ManyToManyField('self', blank=True, related_name="adds_pickablearticles")
    adds_count = models.ForeignKey(CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name="addscount_pickablearticles")

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return f"{self.trait}, {self.basics}, {self.basics_count}, {self.adds}, {self.adds_count}, {self.sort_number}" 


class PickableSet(models.Model):
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE,
        related_name="trait_pickablesets")

    articles = models.ManyToManyField(PickableArticle, blank=True, related_name="articles_pickablesets")
    articles_count = models.ForeignKey(CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name="articlescount_pickablesets")

    def __str__(self):
        return f"{self.trait}, {self.articles}, {self.articles_count}" 


class PickedArticle(models.Model):
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE,
        related_name="trait_pickedarticles")

    basics = models.ManyToManyField('self', blank=True, related_name="basics_pickedarticles")
    basics_count = models.IntegerField(default= 0)

    adds = models.ManyToManyField('self', blank=True, related_name="adds_pickedarticles")
    adds_count = models.IntegerField(default= 0)

    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.trait}, {self.basics}, {self.basics_count}, {self.adds}, {self.adds_count}, {self.date_time}"


class PickedSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_pickedsets")

    trait = models.ForeignKey(Trait, on_delete=models.CASCADE,
        related_name="trait_pickedsets")

    articles = models.ManyToManyField(PickedArticle, blank=True, related_name="articles_pickedsets")
    articles_count = models.IntegerField(default= 0)

    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user}, {self.trait}, {self.articles}, {self.articles_count}, {self.date_time}" 
