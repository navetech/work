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

    order_page_title = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='order_page_title_Setting_related'
    )

    order_page_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='order_page_header_Setting_related'
    )

    cart_page_title = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='cart_page_title_Setting_related'
    )

    cart_page_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='cart_page_header_Setting_related'
    )

    cart_page_items_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='cart_page_items_header_Setting_related'
    )

    cart_page_no_items_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='cart_page_no_items_header_Setting_related'
    )

    success_page_title = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='success_page_title_Setting_related'
    )

    success_page_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='success_page_header_Setting_related'
    )

    success_page_contents_01 = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='success_page_contents_01_Setting_related'
    )

    success_page_contents_02 = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='success_page_contents_02_Setting_related'
    )

    cancel_page_title = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='cancel_page_title_Setting_related'
    )

    cancel_page_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='cancel_page_header_Setting_related'
    )

    cancel_page_contents = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='cancel_page_contents_Setting_related'
    )

    def __str__(self):
        return (
            f'{self.product_title}, '
            f'{self.product_name}, '
            f'{self.menu_page_title}, '
            f'{self.menu_page_header}, '
            f'{self.order_page_title}, '
            f'{self.order_page_header}, '
            f'{self.cart_page_title}, '
            f'{self.cart_page_header}, '
            f'{self.cart_page_items_header}, '
            f'{self.cart_page_no_items_header}, '
            f'{self.success_page_title}, '
            f'{self.success_page_header}, '
            f'{self.success_page_contents_01}, '
            f'{self.success_page_contents_02}, '
            f'{self.cancel_page_title}, '
            f'{self.cancel_page_header}, '
            f'{self.cancel_page_contents}'
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
        to_dict(
            self.order_page_title, dict, key='order_page_title', **settings
        )
        to_dict(
            self.order_page_header, dict, key='order_page_header', **settings
        )
        to_dict(
            self.cart_page_title, dict, key='cart_page_title', **settings
        )
        to_dict(
            self.cart_page_header, dict, key='cart_page_header', **settings
        )
        to_dict(
            self.cart_page_items_header, dict,
            key='cart_page_items_header', **settings
        )
        to_dict(
            self.cart_page_no_items_header, dict,
            key='cart_page_no_items_header', **settings
        )
        to_dict(
            self.success_page_title,
            dict, key='success_page_title', **settings
        )
        to_dict(
            self.success_page_header,
            dict, key='success_page_header', **settings
        )
        to_dict(
            self.success_page_contents_01, dict,
            key='success_page_contents_01', **settings
        )
        to_dict(
            self.success_page_contents_02, dict,
            key='success_page_contents_02', **settings
        )
        to_dict(
            self.cancel_page_title, dict, key='cancel_page_title', **settings
        )
        to_dict(
            self.cancel_page_header, dict, key='cancel_page_header', **settings
        )
        to_dict(
            self.cancel_page_contents, dict,
            key='cancel_page_contents', **settings
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


class OrderBasicCommonFields(CommonFields):
    count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.count}, '
            f'{CommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        CommonFields.to_dict(self, dict, **settings)
        dict['count'] = self.count

        return


class OrderCommonFields(OrderBasicCommonFields):
    plain = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.plain}, '
            f'{OrderBasicCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        OrderBasicCommonFields.to_dict(self, dict, **settings)
        dict['plain'] = self.plain

        return


class OrderSize(OrderBasicCommonFields):
    menu = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderSize_related'
    )

    def cancel(self):
        self.delete()

    def __str__(self):
        return (
            f'{self.menu}, '
            f'{OrderBasicCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        OrderBasicCommonFields.to_dict(self, dict, **settings)

        to_dict(self.menu, dict, key='menu', **settings)

        return


def get_order_size(order_object, size_id):
    if not order_object:
        return None

    if size_id is None:
        return None

    size = Size.objects.filter(id=size_id).first()
    if not size:
        return None

    for order_size in order_object.sizes.all():
        menu_size = order_size.menu

        if size == menu_size:
            return order_size

    return None


class OrderAdding(OrderCommonFields):
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

    def cancel(self):
        cancel_order_flavors(self)
        cancel_order_sizes(self)

        self.delete()

    def __str__(self):
        return (
            f'{self.flavors}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{OrderCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        OrderCommonFields.to_dict(self, dict, **settings)

        dict['flavors'] = to_dict_list(self.flavors, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        to_dict(self.menu, dict, key='menu', **settings)

        return


class OrderFlavor(OrderCommonFields):
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

    def cancel(self):
        cancel_order_addings(self)
        cancel_order_sizes(self)

        self.delete()

    def __str__(self):
        return (
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{OrderCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        OrderCommonFields.to_dict(self, dict, **settings)

        dict['addings'] = to_dict_list(self.addings, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        to_dict(self.menu, dict, key='menu', **settings)

        return


def get_order_flavor(order_object, flavor_id, size_id):
    if not order_object:
        return None

    if flavor_id is None:
        return None

    flavor = Flavor.objects.filter(id=flavor_id).first()
    if not flavor:
        return None

    for order_flavor in order_object.flavors.all():
        menu_flavor = order_flavor.menu

        if flavor == menu_flavor:
            no_components = True

            if menu_flavor.sizes.count() > 0:
                no_components = False

                order_size = get_order_size(order_flavor, size_id)
                if order_size:
                    return order_flavor

            if no_components:
                return order_flavor

    return None


class OrderType(OrderCommonFields):
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

    def cancel(self):
        cancel_order_flavors(self)
        cancel_order_addings(self)
        cancel_order_sizes(self)

        self.delete()

    def __str__(self):
        return (
            f'{self.flavors}, '
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{OrderCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        OrderCommonFields.to_dict(self, dict, **settings)

        dict['flavors'] = to_dict_list(self.flavors, **settings)
        dict['addings'] = to_dict_list(self.addings, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        to_dict(self.menu, dict, key='menu', **settings)

        return


class OrderDish(OrderCommonFields):
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

    def cancel(self):
        cancel_order_types(self)
        cancel_order_flavors(self)
        cancel_order_addings(self)
        cancel_order_sizes(self)

        self.delete()

    def __str__(self):
        return (
            f'{self.types}, '
            f'{self.flavors}, '
            f'{self.addings}, '
            f'{self.sizes}, '
            f'{self.menu}, '
            f'{OrderCommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        OrderCommonFields.to_dict(self, dict, **settings)

        dict['types'] = to_dict_list(self.types, **settings)
        dict['flavors'] = to_dict_list(self.flavors, **settings)
        dict['addings'] = to_dict_list(self.addings, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        to_dict(self.menu, dict, key='menu', **settings)

        return


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

    def cancel(self):
        cancel_order_dishes(self)

        self.delete()

    def __str__(self):
        return (
            f'{self.dishes}, '
            f'{self.user}, '
            f'{self.date_time}, '
            f'{CommonFields.__str__(self)}'
        )

    def to_dict(self, dict, **settings):
        CommonFields.to_dict(self, dict, **settings)

        dict['dishes'] = to_dict_list(self.dishes, **settings)

        return


class HistoricOrder(models.Model):
    order = models.TextField(blank=True)


def cancel_order_sizes(order_object):
    if order_object:
        for order_size in order_object.sizes.all():
            order_size.cancel()


def cancel_order_addings(order_object):
    if order_object:
        for order_adding in order_object.addings.all():
            order_adding.cancel()


def cancel_order_flavors(order_object):
    if order_object:
        for order_flavor in order_object.flavors.all():
            order_flavor.cancel()


def cancel_order_types(order_object):
    if order_object:
        for order_type in order_object.types.all():
            order_type.cancel()


def cancel_order_dishes(order_object):
    if order_object:
        for order_dish in order_object.dishes.all():
            order_dish.cancel()


def create_order_sizes(order_object, menu_object):
    if not order_object:
        return False
    if not menu_object:
        return False

    for size in menu_object.sizes.all():
        order_size = OrderSize(menu=size, count=0)
        order_size.save()

        order_object.sizes.add(order_size)
        order_object.save()

    return True


def create_order_size(order_object, menu_object, size_id):
    if not order_object:
        return None
    if not menu_object:
        return None
    if size_id is None:
        return None

    size = Size.objects.filter(id=size_id).first()
    if not size:
        return None
    if size not in menu_object.sizes.all():
        return None

    order_size = OrderSize(menu=size, count=1)
    order_size.save()

    order_object.sizes.add(order_size)
    order_object.save()

    return order_size


def create_order_flavors(order_object, menu_object):
    if not order_object:
        return False
    if not menu_object:
        return False

    for flavor in menu_object.flavors.all():
        order_flavor = OrderFlavor(menu=flavor, count=0, plain=False)
        order_flavor.save()

        create_order_addings(order_flavor, flavor)
        order_flavor.save()

        create_order_sizes(order_flavor, flavor)
        order_flavor.save()

        order_object.flavors.add(order_flavor)
        order_object.save()

    return True


def create_order_addings(order_object, menu_object):
    if not order_object:
        return False
    if not menu_object:
        return False

    for adding in menu_object.addings.all():
        order_adding = OrderAdding(menu=adding, count=0, plain=False)
        order_adding.save()

        create_order_flavors(order_adding, adding)
        order_adding.save()

        create_order_sizes(order_adding, adding)
        order_adding.save()

        order_object.addings.add(order_adding)
        order_object.save()

    return True


def create_order_flavor(order_object, menu_object, flavor_id, size_id):
    if not order_object:
        return None
    if not menu_object:
        return None
    if flavor_id is None:
        return None

    flavor = Flavor.objects.filter(id=flavor_id).first()
    if not flavor:
        return None
    if flavor not in menu_object.flavors.all():
        return None

    order_flavor = OrderFlavor(menu=flavor, count=1, plain=False)
    order_flavor.save()

    if size_id is not None:
        create_order_size(order_flavor, flavor, size_id)
    else:
        order_flavor.plain = True

    order_flavor.save()

#    if flavor.addings_count.max != 0:
    create_order_addings(order_flavor, flavor)
    order_flavor.save()

    order_object.flavors.add(order_flavor)
    order_object.save()

    return order_flavor


def create_order_type(order_object, menu_object, type_id, flavor_id, size_id):
    if not order_object:
        return None
    if not menu_object:
        return None
    if type_id is None:
        return None

    type = Type.objects.filter(id=type_id).first()
    if not type:
        return None
    if type not in menu_object.types.all():
        return None

    order_type = OrderType(menu=type, count=1, plain=False)
    order_type.save()

    if flavor_id is not None:
        create_order_flavor(order_type, type, flavor_id, size_id)
    elif size_id is not None:
        create_order_size(order_type, type, size_id)
    else:
        order_type.plain = True

    order_type.save()

#    if type.addings_count.max != 0:
    create_order_addings(order_type, type)
    order_type.save()

    order_object.types.add(order_type)
    order_object.save()

    return order_type


def create_order_dish(order, dish_id, type_id, flavor_id, size_id):
    if not order:
        return None
    if dish_id is None:
        return None

    dish = Dish.objects.filter(id=dish_id).first()
    if not dish:
        return None

    order_dish = OrderDish(menu=dish, count=1, plain=False)
    order_dish.save()

    if type_id is not None:
        create_order_type(order_dish, dish, type_id, flavor_id, size_id)
    elif flavor_id is not None:
        create_order_flavor(order_dish, dish, flavor_id, size_id)
    elif size_id is not None:
        create_order_size(order_dish, dish, size_id)
    else:
        order_dish.plain = True

    order_dish.save()

    if dish.addings_count and dish.addings_count.max:
        create_order_addings(order_dish, dish)
        order_dish.save()

    order.dishes.add(order_dish)
    order.save()

    return order_dish


def get_order_dishes(order):
    if not order:
        return []

    return order.dishes.all()


def get_order_dish(order, dish_id, type_id, flavor_id, size_id):
    if not order:
        return None

    if dish_id is None:
        return None

    dish = Dish.objects.filter(id=dish_id).first()
    if not dish:
        return None

    for order_dish in order.dishes.all():
        menu_dish = order_dish.menu

        if dish == menu_dish:
            no_components = True

            if menu_dish.types.count() > 0:
                no_components = False

                order_type = get_order_type(
                    order_dish, type_id, flavor_id, size_id
                )
                if order_type:
                    return order_dish

            if menu_dish.flavors.count() > 0:
                no_components = False

                order_flavor = get_order_flavor(order_dish, flavor_id, size_id)
                if order_flavor:
                    return order_dish

            if menu_dish.sizes.count() > 0:
                no_components = False

                order_size = get_order_size(order_dish, size_id)
                if order_size:
                    return order_dish

            if no_components:
                return order_dish

    order_dish = create_order_dish(order, dish_id, type_id, flavor_id, size_id)

    return order_dish


def create_order(user):
    order = Order(user=user)
    order.save()

    return order


def get_order(user):
    order = Order.objects.filter(user=user).first()
    if not order:
        order = create_order(user=user)

    return order


def get_order_type(order_object, type_id, flavor_id, size_id):
    if not order_object:
        return None

    if type_id is None:
        return None

    type = Type.objects.filter(id=type_id).first()
    if not type:
        return None

    for order_type in order_object.types.all():
        menu_type = order_type.menu

        if type == menu_type:
            no_components = True

            if menu_type.flavors.count() > 0:
                no_components = False

                order_flavor = get_order_flavor(order_type, flavor_id, size_id)
                if order_flavor:
                    return order_type

            if menu_type.sizes.count() > 0:
                no_components = False

                order_size = get_order_size(order_type, size_id)
                if order_size:
                    return order_type

            if no_components:
                return order_type

    return None
