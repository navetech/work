from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Language(models.Model):
    english_name = models.CharField(max_length=64)
    ISO_639_1_code = models.CharField(max_length=2)

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return f"{self.english_name}, {self.ISO_639_1_code}, {self.sort_number}"


class Text(models.Model):
    text = models.CharField(max_length=256)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
        related_name="language_texts")

    basics = models.ManyToManyField('self', blank=True, related_name="basics_texts")

    def __str__(self):
        return f"{self.text}, {self.language}, {self.basics}"


class ISO_4217_CurrencyCode(models.Model):
    entity = models.CharField(max_length=64)
    currency = models.CharField(max_length=64)
    code = models.CharField(max_length=3)
    minor_unit = models.IntegerField(default= 2, blank=True)

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return f"{self.entity}, {self.currency}, {self.code}, {self.minor_unit}, {self.sort_number}"


class Price(models.Model):
    currency = models.ForeignKey(ISO_4217_CurrencyCode, on_delete=models.CASCADE,
        related_name="currency_prices")
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.currency}, {self.value}"


class Trait(models.Model):
    texts = models.ManyToManyField(Text, blank=True, related_name="texts_traits")
    price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.CASCADE,
        related_name="price_traits")

    sort_number = models.FloatField(default=0)

    def __str__(self):
        return f"{self.texts}, {self.price}, {self.sort_number}"


class ArticleCore(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE,
        related_name="article_articlecores")
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE,
        related_name="trait_articlecores")

    def __str__(self):
        return f"{self.article}, {self.trait}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    items = models.ManyToManyField(ArticleCore, blank=True, related_name="items_orders")

    def __str__(self):
        return f"{self.user}, {self.items}"


class Range(models.Model):
    min = models.IntegerField(default= 0, blank=True)
    max = models.IntegerField(default= 0, blank=True)

    def __str__(self):
        return f"{self.min}, {self.max}" 


class Article(models.Model):
    trait = models.ForeignKey('Trait', on_delete=models.CASCADE,
        related_name="trait_articles")

    basics = models.ManyToManyField(ArticleCore, blank=True, related_name="basics_articles")
    basics_range = models.ForeignKey(Range, blank=True, null=True, on_delete=models.CASCADE,
        related_name="basicsrange_articles")

    adds = models.ManyToManyField(ArticleCore, blank=True, related_name="adds_articles")
    adds_range = models.ForeignKey(Range, blank=True, null=True, on_delete=models.CASCADE,
        related_name="addsrange_articles")

    def __str__(self):
        return f"{self.trait}, {self.basics}, {self.basics_range}, {self.adds}, {self.adds_range}" 
