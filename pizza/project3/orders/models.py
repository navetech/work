from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from traits.models import Trait


class CommonInfo(models.Model):
    trait = models.ForeignKey(
        Trait, blank=True, null=True, on_delete=models.CASCADE,
        related_name='trait_CommonInfo_related_%(app_label)s_%(class)s'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.trait}'
        )


class MenuCommonInfo(CommonInfo):
    sort_number = models.FloatField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.sort_number}, '
            f'{CommonInfo.__str__(self)}'
        )


class CountLimit(models.Model):
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return (
            f'{self.min}, '
            f'{self.max}'
        )


class Size(MenuCommonInfo):
    pass

    def __str__(self):
        return (
            f'{MenuCommonInfo.__str__(self)}'
        )


class Adding(MenuCommonInfo):
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
            f'{MenuCommonInfo.__str__(self)}'
        )


class Flavor(MenuCommonInfo):
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
            f'{MenuCommonInfo.__str__(self)}'
        )


class Type(MenuCommonInfo):
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
            f'{MenuCommonInfo.__str__(self)}'
        )


class Dish(MenuCommonInfo):
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
            f'{MenuCommonInfo.__str__(self)}'
        )


class PickedSize(CommonInfo):
    menu = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_PickedSize_related'
    )

    def __str__(self):
        return (
            f'{menu}, '
            f'{CommonInfo.__str__(self)}'
        )


class PickedAdding(CommonInfo):
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
            f'{menu}, '
            f'{CommonInfo.__str__(self)}'
        )


class PickedFlavor(CommonInfo):
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
            f'{menu}, '
            f'{CommonInfo.__str__(self)}'
        )


class PickedType(CommonInfo):
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
            f'{menu}, '
            f'{CommonInfo.__str__(self)}'
        )


class PickedDish(CommonInfo):
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
            f'{menu}, '
            f'{CommonInfo.__str__(self)}'
        )


class Order(CommonInfo):
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
            f'{CommonInfo.__str__(self)}'
        )


class HistoricOrder(models.Model):
    order = models.TextField(blank=True)
