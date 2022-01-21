from django.db import models

# Create your models here.

from django.apps import apps

from django.contrib.auth.models import User


from texts.models import Phrase
from texts.models import Language
from texts.models import Setting as TextSetting
from texts.models import to_dict

from quantities.models import Quantity
from quantities.models import Currency
from quantities.models import Setting as QuantitySetting


class Setting(models.Model):
    product_title = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='product_title_Setting_related'
    )

    product_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='product_name_Setting_related'
    )

    pages_items_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='pages_items_header_Setting_related'
    )

    pages_no_items_header = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='pages_no_items_header_Setting_related'
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
            f'{self.pages_items_header}, '
            f'{self.pages_no_items_header}, '
            f'{self.menu_page_title}, '
            f'{self.menu_page_header}, '
            f'{self.order_page_title}, '
            f'{self.order_page_header}, '
            f'{self.cart_page_title}, '
            f'{self.cart_page_header}, '
            f'{self.success_page_title}, '
            f'{self.success_page_header}, '
            f'{self.success_page_contents_01}, '
            f'{self.success_page_contents_02}, '
            f'{self.cancel_page_title}, '
            f'{self.cancel_page_header}, '
            f'{self.cancel_page_contents}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['product_title'] = to_dict(self.product_title, **settings)
        dict['product_name'] = to_dict(self.product_name, **settings)
        dict['pages_items_header'] = to_dict(
            self.pages_items_header, **settings
        )
        dict['pages_no_items_header'] = to_dict(
            self.pages_no_items_header, **settings
        )
        dict['menu_page_title'] = to_dict(self.menu_page_title, **settings)
        dict['menu_page_header'] = to_dict(self.menu_page_header, **settings)
        dict['order_page_title'] = to_dict(self.order_page_title, **settings)
        dict['order_page_header'] = to_dict(self.order_page_header, **settings)
        dict['cart_page_title'] = to_dict(self.cart_page_title, **settings)
        dict['cart_page_header'] = to_dict(self.cart_page_header, **settings)
        dict['success_page_title'] = to_dict(
            self.success_page_title, **settings
        )
        dict['success_page_header'] = to_dict(
            self.success_page_header, **settings
        )
        dict['success_page_contents_01'] = to_dict(
            self.success_page_contents_01, **settings
        )
        dict['success_page_contents_02'] = to_dict(
            self.success_page_contents_02, **settings
        )
        dict['cancel_page_title'] = to_dict(self.cancel_page_title, **settings)
        dict['cancel_page_header'] = to_dict(
            self.cancel_page_header, **settings
        )
        dict['cancel_page_contents'] = to_dict(
            self.cancel_page_contents, **settings
        )

        return dict


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

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['language'] = to_dict(self.language, **settings)
        dict['currency'] = to_dict(self.currency, **settings)

        return dict

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


class CountLimit(models.Model):
    min = models.IntegerField(default=0, blank=True)
    max = models.IntegerField(default=-1, blank=True)

    def clean(self):
        if self.min < 0:
            self.min = 0

        if self.max >= 0:
            if self.max < self.min:
                self.max = self.min

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return (
            f'{self.min}, '
            f'{self.max}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['min'] = self.min
        dict['max'] = self.max

        return dict


class MenuElementDefinitionFields(models.Model):
    sort_number = models.FloatField(default=0)

    name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='name_%(app_label)s_%(class)s_related'
    )

    long_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='long_name_%(app_label)s_%(class)s_related'
    )

    description = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.CASCADE,
        related_name='descripton_%(app_label)s_%(class)s_related'
    )

    class Meta:
        abstract = True

    def __str__(self):
        first_name = f'{self._meta.model_name}: {self.name}'
        full_name = first_name

        app_label = self._meta.app_label
#        modelos = apps.get_app_config(app_label).get_models()
        modelos = apps.get_models()
        for modelo in modelos:
            model_name = modelo._meta.model_name

            attr = f'{app_label}_{model_name}_related'
            related_name_count = 0
            if hasattr(self, attr):
                related_name_count += 1
                if related_name_count != 1:
                    full_name = first_name
                    break
                else:
                    containers = getattr(self, attr).all()
                    if containers.count() == 1:
                        full_name = full_name + ' ' + f'{containers.first()}'

        return full_name

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['sort_number'] = self.sort_number

        dict['name'] = to_dict(self.name, **settings)
        dict['long_name'] = to_dict(self.long_name, **settings)
        dict['description'] = to_dict(self.description, **settings)

        if container_dict:
            dict['container'] = container_dict

            if 'full name' in container_dict:
                dict['full_name'] = (
                    self.name.words + ' ' + container_dict['full_name']
                )
            else:
                dict['full_name'] = self.name.words

        return dict


class MenuElementFields(MenuElementDefinitionFields):
    quantity = models.ForeignKey(
        Quantity, blank=True, null=True, on_delete=models.CASCADE,
        related_name='quantity_%(app_label)s_%(class)s_related'
    )

    img = models.ImageField(
        upload_to='uploads/static/images',
        default=None, blank=True, null=True
    )

    class Meta:
        abstract = True

    def to_dict(self, container_dict=None, **settings):
        dict = MenuElementDefinitionFields.to_dict(
            self, container_dict, **settings
        )

        dict['quantity'] = to_dict(self.quantity, **settings)

        dict['img'] = {}
        if self.img:
            dict['img']['name'] = self.img.name
            dict['img']['path'] = self.img.path
            dict['img']['url'] = self.img.url
            dict['img']['height'] = self.img.height
            dict['img']['width'] = self.img.width

        return dict


class Size(MenuElementFields):
    pass


class AddingFlavor(MenuElementFields):
    special = models.BooleanField(default=False)

    sizes = models.ManyToManyField(
        Size, blank=True,
        related_name='%(app_label)s_%(class)s_related'
    )

    def __str__(self):
        return (
            f'{MenuElementFields.__str__(self)}, '

            f'Special={self.special}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = MenuElementFields.to_dict(
            self, container_dict, **settings
        )

        dict['special'] = self.special

        dict['sizes'] = menu_elems_to_dict_list(
            dict, self.sizes, 'sort_number', **settings
        )

        return dict


class AddingFlavorSet(MenuElementDefinitionFields):
    flavors = models.ManyToManyField(
        AddingFlavor, blank=True,
        related_name='%(app_label)s_%(class)s_related'
    )

    def to_dict(self, container_dict=None, **settings):
        dict = MenuElementDefinitionFields.to_dict(
            self, container_dict, **settings
        )

        dict['flavors'] = menu_elems_to_dict_list(
            dict, self.flavors, 'sort_number', **settings
        )

        return dict


class Adding(MenuElementFields):
    flavors_set = models.ForeignKey(
        AddingFlavorSet, blank=True, null=True, on_delete=models.CASCADE,
        related_name='flavors_set_Adding_related'
    )

    only_special_flavors = models.BooleanField(default=False)

    flavors_selection_limit = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.CASCADE,
        related_name='flavors_selection_limit_Adding_related'
    )

    def __str__(self):
        return (
            f'{MenuElementFields.__str__(self)}, '

            f'Only Special={self.only_special_flavors}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = MenuElementFields.to_dict(
            self, container_dict, **settings
        )

        dict['flavors_set'] = menu_elem_to_dict(
            dict, self.flavors_set, **settings
        )

        dict['only_special_flavors'] = self.only_special_flavors

        dict['flavors_selection_limit'] = to_dict(
            self.flavors_selection_limit, **settings
        )

        return dict


class FlavorFields(MenuElementFields):
    sizes = models.ManyToManyField(
        Size, blank=True,
        related_name='%(app_label)s_%(class)s_related'
    )

    addings = models.ManyToManyField(
        Adding, blank=True,
        related_name='%(app_label)s_%(class)s_related'
    )

    class Meta:
        abstract = True

    def to_dict(self, container_dict=None, **settings):
        dict = MenuElementFields.to_dict(
            self, container_dict, **settings
        )

        dict['sizes'] = menu_elems_to_dict_list(
            dict, self.sizes, 'sort_number', **settings
        )
        dict['addings'] = menu_elems_to_dict_list(
            dict, self.addings, 'sort_number', **settings
        )

        return dict


class Flavor(FlavorFields):
    pass


class TypeFields(FlavorFields):
    flavors = models.ManyToManyField(
        Flavor, blank=True,
        related_name='%(app_label)s_%(class)s_related'
    )

    class Meta:
        abstract = True

    def to_dict(self, container_dict=None, **settings):
        dict = FlavorFields.to_dict(self, container_dict, **settings)

        dict['flavors'] = menu_elems_to_dict_list(
            dict, self.flavors, 'sort_number', **settings
        )

        return dict


class Type(TypeFields):
    pass


class DishFields(TypeFields):
    types = models.ManyToManyField(
        Type, blank=True,
        related_name='%(app_label)s_%(class)s_related'
    )

    class Meta:
        abstract = True

    def to_dict(self, container_dict=None, **settings):
        dict = TypeFields.to_dict(self, container_dict, **settings)

        dict['types'] = menu_elems_to_dict_list(
            dict, self.types, 'sort_number', **settings
        )

        return dict


class Dish(DishFields):
    pass


class MenuFields(DishFields):
    dishes = models.ManyToManyField(
        Dish, blank=True,
        related_name='%(app_label)s_%(class)s_related'
    )

    class Meta:
        abstract = True

    def to_dict(self, container_dict=None, **settings):
        dict = DishFields.to_dict(self, container_dict, **settings)

        dict['dishes'] = menu_elems_to_dict_list(
            dict, self.dishes, 'sort_number', **settings
        )

        return dict


class Menu(MenuFields):
    pass


def menu_elem_to_dict(container_dict, object, **settings):
    if object:
        dict = object.to_dict(container_dict, **settings)
    else:
        dict = {}

    return dict


def menu_elems_to_dict_list(
    container_dict, manager, *order_by_field_names, **settings
):
    dict_list = []

    objects = manager.all().order_by(*order_by_field_names)
    for object in objects:
        dict = menu_elem_to_dict(container_dict, object, **settings)
        dict_list.append(dict)

    return dict_list


"""
class OrderBasicCommonFields(models.Model):
    count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{self.count}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['count'] = self.count

        return dict

    def check_count(self, range=None):
        count = self.count
        if count < 0:
            count = 0

        if range and range.max >= 0:
            if count > range.max:
                count = range.max

        self.count = count
        self.save()

        return {
            'count': count,
            'in_range': True,
        }


class OrderCommonFields(OrderBasicCommonFields):
    plain = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f'{OrderBasicCommonFields.__str__(self)}, '
            f'{self.plain}, '
        )

    def to_dict(self, **settings):
        dict = OrderBasicCommonFields.to_dict(self, **settings)
        dict['plain'] = self.plain

        return dict


class OrderSize(OrderBasicCommonFields):
    menu = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderSize_related'
    )

    def cancel(self):
        self.delete()

    def __str__(self):
        return (
            f'{OrderBasicCommonFields.__str__(self)}, '
            f'{self.menu}, '
        )

    def to_dict(self, **settings):
        dict = OrderBasicCommonFields.to_dict(self, **settings)

        dict['menu'] = to_dict(self.menu, **settings)

        return dict

    def check_count(self, range=None):
        return super().check_count(range)

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
            f'{OrderCommonFields.__str__(self)}, '
            f'{self.menu}, '
            f'{self.flavors}, '
            f'{self.sizes}, '
        )

    def to_dict(self, **settings):
        dict = OrderCommonFields.to_dict(self, **settings)

        dict['flavors'] = to_dict_list(self.flavors, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        dict['menu'] = to_dict(self.menu, **settings)

        return dict

    def check_count(self, range=None):
        if self.plain:
            return super().check_count(range)

        count = 0
        in_range = True

        check = check_objects_counts(self.flavors.all(), self.menu.flavors_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        check = check_objects_counts(self.sizes.all(), self.menu.sizes_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        if range and count > range.max:
            in_range = False

        return {
            'count': count,
            'in_range': in_range,
        }


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
            f'{OrderCommonFields.__str__(self)}, '
            f'{self.menu}, '
            f'{self.addings}, '
            f'{self.sizes}, '
        )

    def to_dict(self, **settings):
        dict = OrderCommonFields.to_dict(self, **settings)

        dict['addings'] = to_dict_list(self.addings, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        dict['menu'] = to_dict(self.menu, **settings)

        return dict

    def check_count(self, range=None):
        if self.plain:
            return super().check_count(range)

        count = 0
        in_range = True

        check = check_objects_counts(self.sizes.all(), self.menu.sizes_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        check = check_objects_counts(self.addings.all(), self.menu.addings_count)
        if not check['in_range']:
            in_range = False

        return {
            'count': count,
            'in_range': in_range,
        }


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
            f'{OrderCommonFields.__str__(self)}, '
            f'{self.menu}, '
            f'{self.flavors}, '
            f'{self.addings}, '
            f'{self.sizes}, '
        )

    def to_dict(self, **settings):
        dict = OrderCommonFields.to_dict(self, **settings)

        dict['flavors'] = to_dict_list(self.flavors, **settings)
        dict['addings'] = to_dict_list(self.addings, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        dict['menu'] = to_dict(self.menu, **settings)

        return dict

    def check_count(self, range=None):
        if self.plain:
            return super().check_count(range)

        count = 0
        in_range = True

        check = check_objects_counts(self.flavors.all(), self.menu.flavors_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        check = check_objects_counts(self.sizes.all(), self.menu.sizes_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        check = check_objects_counts(self.addings.all(), self.menu.addings_count)
        if not check['in_range']:
            in_range = False

        return {
            'count': count,
            'in_range': in_range,
        }


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
            f'{OrderCommonFields.__str__(self)}, '
            f'{self.menu}, '
            f'{self.types}, '
            f'{self.flavors}, '
            f'{self.addings}, '
            f'{self.sizes}, '
        )

    def to_dict(self, **settings):
        dict = OrderCommonFields.to_dict(self, **settings)

        dict['types'] = to_dict_list(self.types, **settings)
        dict['flavors'] = to_dict_list(self.flavors, **settings)
        dict['addings'] = to_dict_list(self.addings, **settings)
        dict['sizes'] = to_dict_list(self.sizes, **settings)

        dict['menu'] = to_dict(self.menu, **settings)

        return dict

    def check_count(self, range=None):
        if self.plain:
            return super().check_count(range)

        count = 0
        in_range = True

        check = check_objects_counts(self.types.all(), self.menu.types_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        check = check_objects_counts(self.flavors.all(), self.menu.flavors_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        check = check_objects_counts(self.sizes.all(), self.menu.sizes_count)
        count += check['count']
        if not check['in_range']:
            in_range = False

        check = check_objects_counts(self.addings.all(), self.menu.addings_count)
        if not check['in_range']:
            in_range = False

        return {
            'count': count,
            'in_range': in_range,
        }


class Order(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_Order_related'
    )

    date_time = models.DateTimeField(auto_now=True)

    dishes = models.ManyToManyField(
        OrderDish, blank=True,
        related_name='dishes_Order_related'
    )

    def cancel(self):
        cancel_order_dishes(self)

        self.delete()

    def __str__(self):
        return (
            f'{self.user}, '
            f'{self.date_time}, '
            f'{self.dishes}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['dishes'] = to_dict_list(self.dishes, **settings)

        return dict

    def check_count(self):
        return check_objects_counts(self.dishes.all())

class HistoricOrder(models.Model):
    order = models.TextField(blank=True)
"""


def check_objects_counts(objects, range=None):
    count = 0
    in_range = True

    for object in objects:
        check = object.check_count(range)
        count += check['count']
        if not check['in_range']:
            in_range = False

    if range:
        if count < range.min:
            in_range = False
        elif range.max >= 0 and count > range.max:
            in_range = False

    return {
        'count': count,
        'in_range': in_range,
    }


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
    order_sizes = []

    if not order_object:
        return order_sizes
    if not menu_object:
        return order_sizes

    if menu_object.sizes_count and menu_object.sizes_count.max == 0:
        return order_sizes

    for size in menu_object.sizes.all():
        order_size = OrderSize(menu=size, count=0)
        order_size.save()

        order_object.sizes.add(order_size)
        order_object.save()

    order_sizes = order_object.sizes.all()

    return order_sizes


def create_order_flavors(order_object, menu_object):
    order_flavors = []

    if not order_object:
        return order_flavors
    if not menu_object:
        return order_flavors

    if menu_object.flavors_count and menu_object.flavors_count.max == 0:
        return order_flavors

    for flavor in menu_object.flavors.all():
        order_flavor = OrderFlavor(menu=flavor, count=0, plain=True)
        order_flavor.save()

        if len(create_order_addings(order_flavor, flavor)) > 0:
            order_flavor.plain = False
            order_flavor.save()

        if len(create_order_sizes(order_flavor, flavor)) > 0:
            order_flavor.plain = False
            order_flavor.save()

        order_object.flavors.add(order_flavor)
        order_object.save()

    order_flavors = order_object.flavors.all()

    return order_flavors


def create_order_addings(order_object, menu_object):
    order_addings = []

    if not order_object:
        return order_addings
    if not menu_object:
        return order_addings

    if menu_object.addings_count and menu_object.addings_count.max == 0:
        return order_addings

    for adding in menu_object.addings.all():
        order_adding = OrderAdding(menu=adding, count=0, plain=True)
        order_adding.save()

        if len(create_order_flavors(order_adding, adding)) > 0:
            order_adding.plain = False
            order_adding.save()

        if len(create_order_sizes(order_adding, adding)) > 0:
            order_adding.plain = False
            order_adding.save()

        order_object.addings.add(order_adding)
        order_object.save()

    order_addings = order_object.addings.all()

    return order_addings


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

    create_order_addings(order_dish, dish)
    order_dish.save()

    order.dishes.add(order_dish)
    order.save()

    return order_dish


def get_order_dishes(order, dish_id, type_id, flavor_id, size_id):
    order_dishes = []
    if not order:
        return order_dishes

    if dish_id is None:
        return order_dishes

    dish = Dish.objects.filter(id=dish_id).first()
    if not dish:
        return order_dishes

    for order_dish in order.dishes.all():
        menu_dish = order_dish.menu

        if dish == menu_dish:
            if type_id is not None:
                order_types = get_order_types(
                    order_dish, type_id, flavor_id, size_id
                )
                if len(order_types) > 0:
                    order_dishes.append(order_dish)
            elif flavor_id is not None:
                order_flavors = get_order_flavors(
                    order_dish, flavor_id, size_id
                )
                if len(order_flavors) > 0:
                    order_dishes.append(order_dish)
            elif size_id is not None:
                order_sizes = get_order_sizes(
                    order_dish, size_id
                )
                if len(order_sizes) > 0:
                    order_dishes.append(order_dish)
            else:
                order_dishes.append(order_dish)

    return order_dishes


def get_order_types(order, type_id, flavor_id, size_id):
    order_types = []
    if not order:
        return order_types

    if type_id is None:
        return order_types

    type = Type.objects.filter(id=type_id).first()
    if not type:
        return order_types

    for order_type in order.types.all():
        menu_type = order_type.menu

        if type == menu_type:
            if flavor_id is not None:
                order_flavors = get_order_flavors(
                    order_type, flavor_id, size_id
                )
                if len(order_flavors) > 0:
                    order_types.append(order_type)
            elif size_id is not None:
                order_sizes = get_order_sizes(
                    order_type, size_id
                )
                if len(order_sizes) > 0:
                    order_types.append(order_type)
            else:
                order_types.append(order_type)

    return order_types


def get_order_flavors(order, flavor_id, size_id):
    order_flavors = []
    if not order:
        return order_flavors

    if flavor_id is None:
        return order_flavors

    flavor = Flavor.objects.filter(id=flavor_id).first()
    if not flavor:
        return order_flavors

    for order_flavor in order.flavors.all():
        menu_type = order_flavor.menu

        if type == menu_type:
            if size_id is not None:
                order_sizes = get_order_sizes(
                    order_flavor, size_id
                )
                if len(order_sizes) > 0:
                    order_flavors.append(order_flavor)
            else:
                order_flavors.append(order_flavor)

    return order_flavors


def get_order_sizes(order_object, size_id):
    order_sizes = []

    if not order_object:
        return order_sizes

    if size_id is None:
        return order_sizes

    size = Size.objects.filter(id=size_id).first()
    if not size:
        return order_sizes

    for order_size in order_object.sizes.all():
        menu_size = order_size.menu

        if size == menu_size:
            order_sizes.append(order_size)

    return order_sizes


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
