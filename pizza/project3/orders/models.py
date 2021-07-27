from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from traits.models import Trait


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

    def to_dict(self, dict):
        dict['trait'] = self.trait

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

    def to_dict(self, dict):
        CommonFields.to_dict(self,dict)
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

    def to_dict(self, dict):
        dict['min'] = self.min
        dict['max'] = self.max

        return


class Size(MenuCommonFields):
    pass

    def __str__(self):
        return (
            f'{MenuCommonFields.__str__(self)}'
        )

    def to_dict(self, dict):
        MenuCommonFields.to_dict(self, dict)

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

    def to_dict(self, dict):
        MenuCommonFields.to_dict(self, dict)

        dict['sizes'] = to_dict_list(self.sizes, 'sort_number')

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

    def to_dict(self, dict):
        MenuCommonFields.to_dict(self, dict)

        dict['flavors'] = to_dict_list(self.flavors, 'sort_number')

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

    def to_dict(self, dict):
        MenuCommonFields.to_dict(self, dict)

        dict['types'] = to_dict_list(self.types, 'sort_number')
        dict['types_count'] = {}
        if self.types_count:
            self.types_count.to_dict(dict['types_count'])

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


def to_dict_list(manager, *order_by_field_names):
    dict_list = []

    objects = manager.all().order_by(*order_by_field_names)
    for object in objects:
        dict = {}
        object.to_dict(dict)
        dict_list.append(dict)

    return dict_list


