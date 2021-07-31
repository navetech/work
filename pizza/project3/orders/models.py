from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from texts.models import Phrase
from texts.models import Language
from texts.models import Setting as TextSetting
from texts.models import to_dict

from quantities.models import Currency
from quantities.models import Setting as QuantitySetting

from traits.models import Trait
    

def to_dict_list(manager, *order_by_field_names, **settings):
    dict_list = []

    objects = manager.all().order_by(*order_by_field_names)
    for object in objects:
        dict = {}
        object.to_dict(dict, **settings)
        dict_list.append(dict)

    return dict_list


class Setting(models.Model):
    product_title = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='product_title_Setting_related'
    )

    product_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='product_name_Setting_related'
    )

    menu_page_title = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_page_title_Setting_related'
    )

    menu_page_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_page_header_Setting_related'
    )

    def __str__(self):
        return (
            f'{self.product_title}, '
            f'{self.product_name}, '
            f'{self.menu_page_title}, '
            f'{self.menu_page_header}, '
        )

    def to_dict(self, dict, **settings):
        dict['id'] = self.id

        to_dict(self.product_title, dict, key='product_title', **settings)
        to_dict(self.product_name, dict, key='product_name', **settings)
        to_dict(self.menu_page_title, dict, key='menu_page_title', **settings)
        to_dict(self.menu_page_header, dict, key='menu_page_header', **settings)

        return


class UserSetting(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_UserSetting_related'
    )

    language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.CASCADE,
        related_name='language_UserSetting_related'
    )

    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.CASCADE,
        related_name='currency_UserSetting_related'
    )

    def __str__(self):
        return (
            f'{self.user}, '
            f'{self.language}, '
            f'{self.currency}, '
        )


    def to_dict(self, dict, **settings):
        dict['id'] = self.id

        to_dict(self.language, dict, key='language', **settings)
        to_dict(self.currency, dict, key='currency', **settings)

        return

    @classmethod
    def get_first(cls, user):
        settings = cls.objects.filter(user=user).first()
        if not settings:
            language = TextSetting.get_first_language()
            currency = QuantitySetting.get_first_currency()

            if language and currency:
                settings = cls(user=user, language=language, currency=currency)
                settings.save()
            elif language:
                settings = cls(user=user, language=language)
                settings.save()
            elif currency:
                settings = cls(user=user, currency=currency)
                settings.save()
        else:
            if not settings.language or not settings.currency:
                if not settings.language:
                    language = TextSetting.get_first_language()
                    settings.language = language

                if not settings.currency:
                    currency = QuantitySetting.get_first_currency()
                    settings.currency = currency

                settings.save()

        return settings


class CommonFields(models.Model):
    trait = models.ForeignKey(
        Trait, blank=True, null=True, on_delete=models.CASCADE,
        related_name='trait_CommonFields_related_%(app_label)s_%(class)s'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.trait}'
        )

    def to_dict(self, dict, **settings):
        dict['id'] = self.id

        to_dict(self.trait, dict, key='trait', **settings)

        return


class MenuCommonFields(CommonFields):
    sort_number = models.FloatField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{CommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        CommonFields.to_dict(self, dict, **settings)
        dict['sort_number'] = self.sort_number

        return


class CountLimit(models.Model):
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.min}, '
            f'{self.max}'
        )

    def to_dict(self, dict, **settings):
        dict['id'] = self.id

        dict['min'] = self.min
        dict['max'] = self.max

        return


class Size(MenuCommonFields):
    pass

    def __str__(self):
        return (
            f'{MenuCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        MenuCommonFields.to_dict(self, dict, **settings)

        return


class Adding(MenuCommonFields):
    flavors = models.ManyToManyField(
        'Flavor', blank=True,
        related_name='flavors_Adding_related'
    )
    flavors_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='flavors_count_Adding_related'
    )

    sizes = models.ManyToManyField(
        Size, blank=True,
        related_name='sizes_Adding_related'
    )
    sizes_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='sizes_count_Adding_related'
    )

    def __str__(self):
        return (
            f'{self.flavors}, {self.flavors_count}, '
            f'{self.sizes}, {self.sizes_count}, '
            f'{MenuCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        MenuCommonFields.to_dict(self, dict, **settings)

        dict['flavors'] = to_dict_list(self.flavors, 'sort_number', **settings)
        to_dict(self.flavors_count, dict, key='flavors_count', **settings)

        dict['sizes'] = to_dict_list(self.sizes, 'sort_number', **settings)
        to_dict(self.sizes_count, dict, key='sizes_count', **settings)

        return


class Flavor(MenuCommonFields):
    addings = models.ManyToManyField(
        'Adding', blank=True,
        related_name='addings_Flavor_related'
    )
    addings_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='addings_count_Flavor_related'
    )

    sizes = models.ManyToManyField(
        Size, blank=True,
        related_name='sizes_Flavor_related'
    )
    sizes_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='sizes_count_Flavor_related'
    )

    def __str__(self):
        return (
            f'{self.addings}, {self.addings_count}, '
            f'{self.sizes}, {self.sizes_count}, '
            f'{MenuCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        MenuCommonFields.to_dict(self, dict, **settings)

        dict['addings'] = to_dict_list(self.addings, 'sort_number', **settings)
        to_dict(self.addings_count, dict, key='addings_count', **settings)

        dict['sizes'] = to_dict_list(self.sizes, 'sort_number', **settings)
        to_dict(self.sizes_count, dict, key='sizes_count', **settings)

        return


class Type(MenuCommonFields):
    flavors = models.ManyToManyField(
        Flavor, blank=True,
        related_name='flavors_Type_related'
    )
    flavors_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='flavors_count_Type_related'
    )

    addings = models.ManyToManyField(
        Adding, blank=True,
        related_name='addings_Type_related'
    )
    addings_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='addings_count_Type_related'
    )

    sizes = models.ManyToManyField(
        Size, blank=True,
        related_name='sizes_Type_related'
    )
    sizes_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='sizes_count_Type_related'
    )

    def __str__(self):
        return (
            f'{self.flavors}, {self.flavors_count}, '
            f'{self.addings}, {self.addings_count}, '
            f'{self.sizes}, {self.sizes_count}, '
            f'{MenuCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        MenuCommonFields.to_dict(self, dict, **settings)

        dict['flavors'] = to_dict_list(self.flavors, 'sort_number', **settings)
        to_dict(self.flavors_count, dict, key='flavors_count', **settings)

        dict['addings'] = to_dict_list(self.addings, 'sort_number', **settings)
        to_dict(self.addings_count, dict, key='addings_count', **settings)

        dict['sizes'] = to_dict_list(self.sizes, 'sort_number', **settings)
        to_dict(self.sizes_count, dict, key='sizes_count', **settings)

        return


class Dish(MenuCommonFields):
    types = models.ManyToManyField(
        Type, blank=True,
        related_name='types_Dish_related'
    )
    types_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='types_count_Dish_related'
    )

    flavors = models.ManyToManyField(
        Flavor, blank=True,
        related_name='flavors_Dish_related'
    )
    flavors_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='flavors_count_Dish_related'
    )

    addings = models.ManyToManyField(
        Adding, blank=True,
        related_name='addings_Dish_related'
    )
    addings_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='addings_count_Dish_related'
    )

    sizes = models.ManyToManyField(
        Size, blank=True,
        related_name='sizes_Dish_related'
    )
    sizes_count = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='sizes_count_Dish_related'
    )

    def __str__(self):
        return (
            f'{self.types}, {self.types_count}, '
            f'{self.flavors}, {self.flavors_count}, '
            f'{self.addings}, {self.addings_count}, '
            f'{self.sizes}, {self.sizes_count}, '
            f'{MenuCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        MenuCommonFields.to_dict(self, dict, **settings)

        dict['types'] = to_dict_list(self.types, 'sort_number', **settings)
        to_dict(self.types_count, dict, key='types_count', **settings)

        dict['flavors'] = to_dict_list(self.flavors, 'sort_number', **settings)
        to_dict(self.flavors_count, dict, key='flavors_count', **settings)

        dict['addings'] = to_dict_list(self.addings, 'sort_number', **settings)
        to_dict(self.addings_count, dict, key='addings_count', **settings)

        dict['sizes'] = to_dict_list(self.sizes, 'sort_number', **settings)
        to_dict(self.sizes_count, dict, key='sizes_count', **settings)

        return


class PickedSize(CommonFields):
    menu = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_PickedSize_related'
    )

    def __str__(self):
        return (
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


class PickedAdding(CommonFields):
    flavors = models.ManyToManyField(
        'PickedFlavor', blank=True,
        related_name='flavors_PickedAdding_related'
    )

    sizes = models.ManyToManyField(
        PickedSize, blank=True,
        related_name='sizes_PickedAdding_related'
    )

    menu = models.ForeignKey(
        Adding, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_PickedAdding_related'
    )

    def __str__(self):
        return (
            f'{self.flavors}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


class PickedFlavor(CommonFields):
    addings = models.ManyToManyField(
        'PickedAdding', blank=True,
        related_name='addings_PickedFlavor_related'
    )

    sizes = models.ManyToManyField(
        PickedSize, blank=True,
        related_name='sizes_PickedFlavor_related'
    )

    menu = models.ForeignKey(
        Flavor, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_PickedFlavor_related'
    )

    def __str__(self):
        return (
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


class PickedType(CommonFields):
    flavors = models.ManyToManyField(
        PickedFlavor, blank=True,
        related_name='flavors_PickedType_related'
    )

    addings = models.ManyToManyField(
        PickedAdding, blank=True,
        related_name='addings_PickedType_related'
    )

    sizes = models.ManyToManyField(
        PickedSize, blank=True,
        related_name='sizes_PickedType_related'
    )

    menu = models.ForeignKey(
        Type, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_PickedType_related'
    )

    def __str__(self):
        return (
            f'{self.flavors}, '
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


class PickedDish(CommonFields):
    types = models.ManyToManyField(
        PickedType, blank=True,
        related_name='types_PickedDish_related'
    )

    flavors = models.ManyToManyField(
        PickedFlavor, blank=True,
        related_name='flavors_PickedDish_related'
    )

    addings = models.ManyToManyField(
        PickedAdding, blank=True,
        related_name='addings_PickedDish_related'
    )

    sizes = models.ManyToManyField(
        PickedSize, blank=True,
        related_name='sizes_PickedDish_related'
    )

    menu = models.ForeignKey(
        Dish, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_PickedDish_related'
    )

    def __str__(self):
        return (
            f'{self.types}, '
            f'{self.flavors}, '
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


class Order(CommonFields):
    dishes = models.ManyToManyField(
        PickedDish, blank=True,
        related_name='dishes_Order_related'
    )

    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_Order_related'
    )

    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f'{self.dishes}, '
            f'{self.user}, {self.date_time}, '
            f'{CommonFields.__str__(self)}'
        )


class HistoricOrder(models.Model):
    order = models.TextField(blank=True)
