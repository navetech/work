from django.db import models

# Create your models here.

from django.contrib.auth.models import User

from texts.models import Phrase
from texts.models import Language
from texts.models import Setting as TextSetting
from texts.models import to_dict_list
from texts.models import to_dict

from quantities.models import Currency
from quantities.models import Setting as QuantitySetting

from traits.models import Trait


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
            f'{self.menu_page_header}'
        )

    def to_dict(self, dict, **settings):
        dict['id'] = self.id

        to_dict(self.product_title, dict, key='product_title', **settings)
        to_dict(self.product_name, dict, key='product_name', **settings)
        to_dict(
            self.menu_page_title, dict, key='menu_page_title', **settings
        )
        to_dict(
            self.menu_page_header, dict, key='menu_page_header', **settings
        )

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
            f'{self.currency}'
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
            f'{self.flavors}, '
            f'{self.flavors_count}, '
            f'{self.sizes}, '
            f'{self.sizes_count}, '
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
            f'{self.addings}, '
            f'{self.addings_count}, '
            f'{self.sizes}, '
            f'{self.sizes_count}, '
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
            f'{self.flavors}, '
            f'{self.flavors_count}, '
            f'{self.addings}, '
            f'{self.addings_count}, '
            f'{self.sizes}, '
            f'{self.sizes_count}, '
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
            f'{self.types}, '
            f'{self.types_count}, '
            f'{self.flavors}, '
            f'{self.flavors_count}, '
            f'{self.addings}, '
            f'{self.addings_count}, '
            f'{self.sizes}, '
            f'{self.sizes_count}, '
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


class OrderSize(CommonFields):
    menu = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderSize_related'
    )

    def __str__(self):
        return (
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


def get_order_size(order_object, size_id):
    print('get_order_size')
    if not order_object:
        return None

    if not size_id and size_id != 0:
        return None

    size = Type.objects.filter(id=size_id).first()
    if not size:
        return None

    for order_size in order_object.sizes.all():
        menu_size = order_size.menu
        print('befor if')

        if size == menu_size:
            print('inside if')
            return order_size

    return None


class OrderAdding(CommonFields):
    flavors = models.ManyToManyField(
        'OrderFlavor', blank=True,
        related_name='flavors_OrderAdding_related'
    )

    sizes = models.ManyToManyField(
        OrderSize, blank=True,
        related_name='sizes_OrderAdding_related'
    )

    menu = models.ForeignKey(
        Adding, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderAdding_related'
    )

    def __str__(self):
        return (
            f'{self.flavors}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


class OrderFlavor(CommonFields):
    addings = models.ManyToManyField(
        'OrderAdding', blank=True,
        related_name='addings_OrderFlavor_related'
    )

    sizes = models.ManyToManyField(
        OrderSize, blank=True,
        related_name='sizes_OrderFlavor_related'
    )

    menu = models.ForeignKey(
        Flavor, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderFlavor_related'
    )

    def __str__(self):
        return (
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


def get_order_flavor(order_object, flavor_id, size_id):
    print('get_order_flavor')
    if not order_object:
        return None

    if not flavor_id and flavor_id != 0:
        return None

    flavor = Type.objects.filter(id=flavor_id).first()
    if not flavor:
        return None

    for order_flavor in order_object.flavors.all():
        menu_flavor = order_flavor.menu

        if flavor == menu_flavor:
            no_components = True
            if menu_flavor.sizes:
                no_components = False

                order_size = get_order_size(order_flavor, size_id)
                print('order_size')
                print(order_size.id)
                print(order_size)
                if order_size:
                    return order_flavor

            if no_components:
                return order_flavor

    return None


class OrderType(CommonFields):
    flavors = models.ManyToManyField(
        OrderFlavor, blank=True,
        related_name='flavors_OrderType_related'
    )

    addings = models.ManyToManyField(
        OrderAdding, blank=True,
        related_name='addings_OrderType_related'
    )

    sizes = models.ManyToManyField(
        OrderSize, blank=True,
        related_name='sizes_OrderType_related'
    )

    menu = models.ForeignKey(
        Type, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderType_related'
    )

    def __str__(self):
        return (
            f'{self.flavors}, '
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{CommonFields.__str__(self)}'
        )


def get_order_type(order_object, type_id, flavor_id, size_id):
    print('get_order_type')
    if not order_object:
        return None

    if not type_id and type_id != 0:
        return None

    type = Type.objects.filter(id=type_id).first()
    if not type:
        return None

    for order_type in order_object.types.all():
        menu_type = order_type.menu

        if type == menu_type:
            no_components = True

            if menu_type.flavors:
                no_components = False

                order_flavor = get_order_flavor(order_type, flavor_id, size_id)
                if order_flavor:
                    return order_type

            if menu_type.sizes:
                no_components = False

                order_size = get_order_size(order_type, size_id)
                if order_size:
                    return order_type

            if no_components:
                return order_type

    return None


class OrderDish(CommonFields):
    types = models.ManyToManyField(
        OrderType, blank=True,
        related_name='types_OrderDish_related'
    )

    flavors = models.ManyToManyField(
        OrderFlavor, blank=True,
        related_name='flavors_OrderDish_related'
    )

    addings = models.ManyToManyField(
        OrderAdding, blank=True,
        related_name='addings_OrderDish_related'
    )

    sizes = models.ManyToManyField(
        OrderSize, blank=True,
        related_name='sizes_OrderDish_related'
    )

    menu = models.ForeignKey(
        Dish, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderDish_related'
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


def create_order_size(order_object, size_id):
    if size_id is None:
        return None

    size = Size.objects.filter(id=size_id).first()
    if not size:
        return None

    order_size = OrderSize(menu=size)
    order_size.save()

    order_object.sizes.add(order_size)
    order_object.save()

#    print(order_size)
#    print(order_size.id)

    return order_size


def create_order_flavor(order_object, flavor_id, size_id):
    if flavor_id is None:
        return None

    flavor = Flavor.objects.filter(id=flavor_id).first()
    if not flavor:
        return None

    order_flavor = OrderFlavor(menu=flavor)
    order_flavor.save()

    if size_id is not None:
        create_order_size(order_flavor, size_id)

    order_object.flavors.add(order_flavor)
    order_object.save()

    return order_flavor


def create_order_type(order_object, type_id, flavor_id, size_id):
    if type_id is None:
        return None

    type = Type.objects.filter(id=type_id).first()
    if not type:
        return None

    order_type = OrderType(menu=type)
    order_type.save()

    if flavor_id is not None:
        create_order_flavor(order_type, flavor_id, size_id)
    elif size_id is not None:
        create_order_size(order_type, size_id)

    order_object.types.add(order_type)
    order_object.save()

    return order_type


def create_order_dish(order, dish_id, type_id, flavor_id, size_id):
    print('create_order_dish')
    if dish_id is None:
        return None

    dish = Dish.objects.filter(id=dish_id).first()
    if not dish:
        return None

    order_dish = OrderDish(menu=dish)
    order_dish.save()

    if type_id is not None:
        create_order_type(order_dish, type_id, flavor_id, size_id)
    elif flavor_id is not None:
        create_order_flavor(order_dish, flavor_id, size_id)
    elif size_id is not None:
        create_order_size(order_dish, size_id)

    order.dishes.add(order_dish)
    order.save()

    return order_dish


def get_order_dish(order, dish_id, type_id, flavor_id, size_id):
    print('get_order_dish')
    if not order:
        return None

    if dish_id is None:
        return None

    dish = Dish.objects.filter(id=dish_id).first()
    if not dish:
        return None

    for order_dish in order.dishes.all():
        menu_dish = order_dish.menu
        print('dishId')
        print(dish.id, menu_dish.id)
        return order_dish

        if dish == menu_dish:
            no_components = True

            if menu_dish.types:
                no_components = False

                order_type = get_order_type(
                    order_dish, type_id, flavor_id, size_id
                )
                if order_type:
                    return order_dish

            if menu_dish.flavors:
                no_components = False

                order_flavor = get_order_flavor(order_dish, flavor_id, size_id)
                if order_flavor:
                    return order_dish

            if menu_dish.sizes:
                no_components = False

                order_size = get_order_size(order_dish, size_id)
                if order_size:
                    return order_dish

            if no_components:
                return order_dish

    order_dish = create_order_dish(order, dish_id, type_id, flavor_id, size_id)

    return order_dish


class Order(CommonFields):
    dishes = models.ManyToManyField(
        OrderDish, blank=True,
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
            f'{self.user}, '
            f'{self.date_time}, '
            f'{CommonFields.__str__(self)}'
        )


def create_order(user):
    order = Order(user=user)
    order.save()

    return order


def get_order(user):
    order = Order.objects.filter(user=user).first()
    if not order:
        order = create_order(user=user)

    return order


class HistoricOrder(models.Model):
    order = models.TextField(blank=True)
