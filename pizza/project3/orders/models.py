from django.db import models

# Create your models here.

from django.apps import apps

from django.contrib.auth.models import User


from texts.models import Phrase
from texts.models import Language
from texts.models import Setting as TextSetting
from texts.models import to_dict, to_dict_list

from quantities.models import Quantity
from quantities.models import Currency
from quantities.models import Setting as QuantitySetting


class Setting(models.Model):
    product_name = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='product_name_Setting_related'
    )

    home_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='home_label_Setting_related'
    )

    menu_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='menu_label_Setting_related'
    )

    cart_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='cart_label_Setting_related'
    )

    register_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='register_label_Setting_related'
    )

    unregister_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='unregister_label_Setting_related'
    )

    login_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='login_label_Setting_related'
    )

    logout_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='logout_label_Setting_related'
    )

    username_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='username_label_Setting_related'
    )

    password_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='password_label_Setting_related'
    )

    cancel_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='cancel_label_Setting_related'
    )

    confirm_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='confirm_label_Setting_related'
    )

    invalid_credentials_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='invalid_credentials_label_Setting_related'
    )

    items_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='items_label_Setting_related'
    )

    no_items_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='no_items_label_Setting_related'
    )

    special_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='special_label_Setting_related'
    )

    ready_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='ready_label_Setting_related'
    )

    not_ready_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='not_ready_label_Setting_related'
    )

    choose_more_options_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='choose_more_options_label_Setting_related'
    )

    choose_less_options_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='choose_less_options_label_Setting_related'
    )

    choose_or_not_options_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='choose_or_not_options_label_Setting_related'
    )

    choose_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='choose_label_Setting_related'
    )

    choose_from_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='choose_from_label_Setting_related'
    )

    choose_up_to_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='choose_up_to_label_Setting_related'
    )

    choose_at_least_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='choose_at_least_label_Setting_related'
    )

    up_to_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='up_to_label_Setting_related'
    )

    option_s_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='option_s_label_Setting_related'
    )

    options_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='options_label_Setting_related'
    )

    checkout_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='checkout_label_Setting_related'
    )

    clear_cart_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='clear_cart_label_Setting_related'
    )

    show_cart_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='show_cart_label_Setting_related'
    )

    menus_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='menus_label_Setting_related'
    )

    order_item_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='order_item_page_label_Setting_related'
    )

    success_page_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='success_page_label_Setting_related'
    )

    success_page_contents_01 = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='success_page_contents_01_Setting_related'
    )

    success_page_contents_02 = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='success_page_contents_02_Setting_related'
    )

    cancel_page_label = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='cancel_page_label_Setting_related'
    )

    cancel_page_contents = models.ForeignKey(
        Phrase, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='cancel_page_contents_Setting_related'
    )

    def __str__(self):
        return (
            f'{self.product_name}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['product_name'] = to_dict(self.product_name, **settings)

        dict['home_label'] = to_dict(self.home_label, **settings)
        dict['menu_label'] = to_dict(self.menu_label, **settings)
        dict['cart_label'] = to_dict(self.cart_label, **settings)

        dict['register_label'] = to_dict(self.register_label, **settings)
        dict['unregister_label'] = to_dict(self.unregister_label, **settings)
        dict['login_label'] = to_dict(self.login_label, **settings)
        dict['logout_label'] = to_dict(self.logout_label, **settings)

        dict['username_label'] = to_dict(self.username_label, **settings)
        dict['password_label'] = to_dict(self.password_label, **settings)
        dict['cancel_label'] = to_dict(self.cancel_label, **settings)
        dict['confirm_label'] = to_dict(self.confirm_label, **settings)
        dict['invalid_credentials_label'] = to_dict(
            self.invalid_credentials_label, **settings
        )

        dict['items_label'] = to_dict(self.items_label, **settings)
        dict['no_items_label'] = to_dict(self.no_items_label, **settings)

        dict['special_label'] = to_dict(self.special_label, **settings)

        dict['ready_label'] = to_dict(self.ready_label, **settings)
        dict['not_ready_label'] = to_dict(self.not_ready_label, **settings)
        dict['choose_more_options_label'] = to_dict(
            self.choose_more_options_label, **settings
        )
        dict['choose_less_options_label'] = to_dict(
            self.choose_less_options_label, **settings
        )
        dict['choose_or_not_options_label'] = to_dict(
            self.choose_or_not_options_label, **settings
        )
        dict['choose_label'] = to_dict(self.choose_label, **settings)
        dict['choose_from_label'] = to_dict(self.choose_from_label, **settings)
        dict['choose_up_to_label'] = to_dict(
            self.choose_up_to_label, **settings
        )
        dict['choose_at_least_label'] = to_dict(
            self.choose_at_least_label, **settings
        )

        dict['up_to_label'] = to_dict(self.up_to_label, **settings)
        dict['option_s_label'] = to_dict(self.option_s_label, **settings)
        dict['options_label'] = to_dict(self.options_label, **settings)

        dict['checkout_label'] = to_dict(self.checkout_label, **settings)
        dict['clear_cart_label'] = to_dict(self.clear_cart_label, **settings)
        dict['show_cart_label'] = to_dict(self.show_cart_label, **settings)
        dict['menus_label'] = to_dict(self.menus_label, **settings)
        dict['order_item_label'] = to_dict(self.order_item_label, **settings)

        dict['success_page_label'] = to_dict(
            self.success_page_label, **settings
        )
        dict['success_page_contents_01'] = to_dict(
            self.success_page_contents_01, **settings
        )
        dict['success_page_contents_02'] = to_dict(
            self.success_page_contents_02, **settings
        )

        dict['cancel_page_label'] = to_dict(self.cancel_page_label, **settings)
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


def adjust_count_limit_dict(limit):
    if not limit:
        min = 0
        max = -1
    else:
        if 'min' in limit and limit['min'] and limit['min'] >= 0:
            min = limit['min']
        else:
            min = 0

        if 'max' not in limit:
            max = -1
        else:
            if limit['max']:
                if limit['max'] < 0:
                    max = -1
                elif limit['max'] >= min:
                    max = limit['max']
                else:
                    max = min
            elif limit['max'] == 0:
                max = min
            else:
                max = -1

    count_limit = {
        'min': min,
        'max': max,
    }

    return count_limit


def adjust_count_limit(limit_obj):
    limit = to_dict(limit_obj)

    count_limit = adjust_count_limit_dict(limit)

    return count_limit


class CountLimit(models.Model):
    min = models.IntegerField(default=0, blank=True)
    max = models.IntegerField(default=-1, blank=True)

    def clean(self):
        limit = adjust_count_limit(self)

        self.min = limit['min']
        self.max = limit['max']

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


def build_elem_full_name(elem, container_dict):
    full_name = elem.name.words

    if container_dict:
        if 'full_name' in container_dict:
            full_name += (
                ' ' + container_dict['full_name']
            )

    return full_name


def elem_to_dict(container_dict, object, **settings):
    if object:
        dict = object.to_dict(container_dict, **settings)
    else:
        dict = {}

    return dict


def elems_to_dict_list(
    container_dict, manager, *order_by_field_names, **settings
):
    dict_list = []

    if manager:
        objects = manager.all().order_by(*order_by_field_names)
        for object in objects:
            dict = elem_to_dict(container_dict, object, **settings)
            if dict:
                dict_list.append(dict)

    return dict_list


def order_item_elems_to_dict_list(
    container_dict, manager, **settings
):
    dict_list = elems_to_dict_list(
        container_dict, manager, 'elem__sort_number', **settings
    )

    return dict_list


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

        dict['full_name'] = build_elem_full_name(self, container_dict)

        if container_dict:
            dict['container'] = container_dict

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


class AddingFlavorSize(MenuElementFields):
    special = models.BooleanField(default=False)

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

        return dict


class AddingFlavor(MenuElementFields):
    special = models.BooleanField(default=False)

    sizes = models.ManyToManyField(
        AddingFlavorSize, blank=True,
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

        dict['sizes'] = elems_to_dict_list(
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

        dict['flavors'] = elems_to_dict_list(
            dict, self.flavors, 'sort_number', **settings
        )

        return dict


class Adding(MenuElementFields):
    flavors_set = models.ForeignKey(
        AddingFlavorSet, blank=True, null=True, on_delete=models.CASCADE,
        related_name='flavors_set_Adding_related'
    )

    only_special_selection = models.BooleanField(default=False)

    flavors_selection_limit = models.ForeignKey(
        CountLimit, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='flavors_selection_limit_Adding_related'
    )

    def __str__(self):
        return (
            f'{MenuElementFields.__str__(self)}, '

            f'Only Special={self.only_special_selection}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = MenuElementFields.to_dict(
            self, container_dict, **settings
        )

        dict['flavors_set'] = elem_to_dict(
            dict, self.flavors_set, **settings
        )

        dict['only_special_selection'] = self.only_special_selection

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

        dict['sizes'] = elems_to_dict_list(
            dict, self.sizes, 'sort_number', **settings
        )
        dict['addings'] = elems_to_dict_list(
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

        dict['flavors'] = elems_to_dict_list(
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

        dict['types'] = elems_to_dict_list(
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

        dict['dishes'] = elems_to_dict_list(
            dict, self.dishes, 'sort_number', **settings
        )

        return dict


class Menu(MenuFields):
    pass


class OrderSize(models.Model):
    elem = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderSize_related'
    )

    def cancel(self):
        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        return dict


class OrderAddingFlavorSize(models.Model):
    elem = models.ForeignKey(
        AddingFlavorSize, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderAddigFlavorSize_related'
    )

    selected = models.BooleanField(default=False)

    def cancel(self):
        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        dict['selected'] = self.selected

        return dict


class OrderAddingFlavor(models.Model):
    elem = models.ForeignKey(
        AddingFlavor, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderAddigFlavor_related'
    )

    sizes = models.ManyToManyField(
        OrderAddingFlavorSize, blank=True,
        related_name='sizes_OrderAddingFlavor_related'
    )

    sizes_selection_count = models.IntegerField(default=0, blank=True)

    selected = models.BooleanField(default=False)

    def cancel(self):
        for size in self.sizes.all():
            size.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        dict['sizes'] = order_item_elems_to_dict_list(
            dict, self.sizes,  **settings
        )

        dict['sizes_selection_count'] = self.sizes_selection_count

        dict['selected'] = self.selected

        return dict


class OrderAdding(models.Model):
    elem = models.ForeignKey(
        Adding, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderAdding_related'
    )

    flavors = models.ManyToManyField(
        OrderAddingFlavor, blank=True,
        related_name='flavors_OrderAdding_related'
    )

    flavors_selection_count = models.IntegerField(default=0, blank=True)

    def cancel(self):
        for flavor in self.flavors.all():
            flavor.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        dict['flavors'] = order_item_elems_to_dict_list(
            dict, self.flavors,  **settings
        )

        dict['flavors_selection_count'] = self.flavors_selection_count

        return dict


class OrderFlavor(models.Model):
    elem = models.ForeignKey(
        Flavor, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderFlavor_related'
    )

    addings = models.ManyToManyField(
        OrderAdding, blank=True,
        related_name='addings_OrderFlavor_related'
    )

    def cancel(self):
        for adding in self.addings.all():
            adding.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        dict['addings'] = order_item_elems_to_dict_list(
            dict, self.addings,  **settings
        )

        return dict


class OrderType(models.Model):
    elem = models.ForeignKey(
        Type, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderType_related'
    )

    addings = models.ManyToManyField(
        OrderAdding, blank=True,
        related_name='addings_OrderType_related'
    )

    def cancel(self):
        for adding in self.addings.all():
            adding.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        dict['addings'] = order_item_elems_to_dict_list(
            dict, self.addings,  **settings
        )

        return dict


class OrderDish(models.Model):
    elem = models.ForeignKey(
        Dish, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderDish_related'
    )

    addings = models.ManyToManyField(
        OrderAdding, blank=True,
        related_name='addings_OrderDish_related'
    )

    def cancel(self):
        for adding in self.addings.all():
            adding.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        dict['addings'] = order_item_elems_to_dict_list(
            dict, self.addings,  **settings
        )

        return dict


class OrderMenu(models.Model):
    elem = models.ForeignKey(
        Menu, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderMenu_related'
    )

    addings = models.ManyToManyField(
        OrderAdding, blank=True,
        related_name='addings_OrderMenu_related'
    )

    def cancel(self):
        for adding in self.addings.all():
            adding.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, container_dict=None, **settings):
        dict = {}

        dict['id'] = self.id

        dict['full_name'] = build_elem_full_name(self.elem, container_dict)

        if container_dict:
            dict['container'] = container_dict

        dict['elem'] = elem_to_dict(
            dict, self.elem, **settings
        )

        dict['addings'] = order_item_elems_to_dict_list(
            dict, self.addings,  **settings
        )

        return dict


class OrderItem(models.Model):
    count = models.IntegerField(default=1, blank=True)

    menu = models.ForeignKey(
        OrderMenu, blank=True, null=True, on_delete=models.CASCADE,
        related_name='menu_OrderItem_related'
    )

    dish = models.ForeignKey(
        OrderDish, blank=True, null=True, on_delete=models.CASCADE,
        related_name='dish_OrderItem_related'
    )

    type = models.ForeignKey(
        OrderType, blank=True, null=True, on_delete=models.CASCADE,
        related_name='type_OrderItem_related'
    )

    flavor = models.ForeignKey(
        OrderFlavor, blank=True, null=True, on_delete=models.CASCADE,
        related_name='flavor_OrderItem_related'
    )

    size = models.ForeignKey(
        OrderSize, blank=True, null=True, on_delete=models.CASCADE,
        related_name='size_OrderItem_related'
    )

    def cancel(self):
        if self.size:
            self.size.cancel()
        if self.flavor:
            self.flavor.cancel()
        if self.type:
            self.type.cancel()
        if self.dish:
            self.dish.cancel()
        if self.menu:
            self.menu.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.menu}, '
            f'{self.dish}, '
            f'{self.type}, '
            f'{self.flavor}, '
            f'{self.size}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['count'] = self.count

        dict['menu'] = to_dict(self.menu, **settings)
        dict['dish'] = to_dict(self.dish, **settings)
        dict['type'] = to_dict(self.type, **settings)
        dict['flavor'] = to_dict(self.flavor, **settings)
        dict['size'] = to_dict(self.size, **settings)

        return dict


class Order(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_Order_related'
    )

    date_time = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=64, blank=True)

    items = models.ManyToManyField(
        OrderItem, blank=True,
        related_name='items_Order_related'
    )

    def cancel(self):
        for item in self.items.all():
            item.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.user}, '
            f'{self.date_time}, '
            f'{self.status}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['items'] = to_dict_list(self.items, **settings)

        return dict


"""
class HistoricOrder(models.Model):
    order = models.TextField(blank=True)
"""


def create_order_adding_flavor_size(adding_flavor_size, selected):
    order_elem = OrderAddingFlavorSize(
        elem=adding_flavor_size, selected=selected
    )
    if order_elem:
        order_elem.save()

    return order_elem


def create_order_adding_flavor(adding_flavor, selected):
    order_elem = OrderAddingFlavor(
        elem=adding_flavor, selected=selected,
        sizes_selection_count=0
    )
    if order_elem:
        order_elem.save()

        adding_flavor_sizes = adding_flavor.sizes.all()
        for adding_flavor_size in adding_flavor_sizes:
            if (
                adding_flavor_size.special and
                order_elem.selected and
                order_elem.sizes_selection_count < 1
            ):
                order_elem.sizes_selection_count += 1
                order_elem.save()
                size_selected = True
            else:
                size_selected = False

            order_adding_flavor_size = create_order_adding_flavor_size(
                adding_flavor_size, size_selected
            )
            order_elem.sizes.add(order_adding_flavor_size)
            order_elem.save()

        if order_elem.selected and order_elem.sizes_selection_count < 1:
            if order_elem.sizes.count() > 0:
                order_adding_flavor_size = order_elem.sizes.first()
                order_adding_flavor_size.selected = True
                order_adding_flavor_size.save()

                order_elem.sizes_selection_count += 1
                order_elem.save()

    return order_elem


def create_order_adding(adding):
    order_elem = None

    if not adding.flavors_set:
        return order_elem

    if adding.flavors_set.flavors.count() < 1:
        return order_elem

    if (
        adding.flavors_selection_limit and
        adding.flavors_selection_limit.max == 0
    ):
        return order_elem

    order_elem = OrderAdding(elem=adding, flavors_selection_count=0)
    if order_elem:
        order_elem.save()

        if adding.flavors_set:
            adding_flavors = adding.flavors_set.flavors.all()
            for adding_flavor in adding_flavors:
                if adding_flavor.special and adding.only_special_selection:
                    selected = True
                    order_elem.flavors_selection_count += 1
                    order_elem.save()
                else:
                    selected = False

                order_adding_flavor = create_order_adding_flavor(
                    adding_flavor, selected
                )
                order_elem.flavors.add(order_adding_flavor)
                order_elem.save()

    return order_elem


def create_order_elem(elem_id, elem_class, order_elem_class):
    elem = elem_class.objects.filter(id=elem_id).first()
    if elem:
        order_elem = order_elem_class(elem=elem)
        if order_elem:
            order_elem.save()
            for adding in elem.addings.all():
                order_adding = create_order_adding(adding)
                order_elem.addings.add(order_adding)
                order_elem.save()
    else:
        order_elem = None

    return order_elem


def create_order_size(size_id):
    elem = Size.objects.filter(id=size_id).first()
    if elem:
        order_elem = OrderSize(elem=elem)
        if order_elem:
            order_elem.save()
    else:
        order_elem = None

    return order_elem


def create_order_item(
    menu_id, dish_id, type_id, flavor_id, size_id
):
    menu = create_order_elem(menu_id, Menu, OrderMenu)
    dish = create_order_elem(dish_id, Dish, OrderDish)
    type = create_order_elem(type_id, Type, OrderType)
    flavor = create_order_elem(flavor_id, Flavor, OrderFlavor)
    size = create_order_size(size_id)

    if menu or dish or type or flavor or size:
        order_item = OrderItem(
            count=1,
            menu=menu, dish=dish, type=type,
            flavor=flavor, size=size
        )
        order_item.save()
    else:
        order_item = None

    return order_item


def create_order_item_for_user(
        menu_id, dish_id, type_id, flavor_id, size_id,
        user, status='InCart'
):
    order_item = create_order_item(
        menu_id, dish_id, type_id, flavor_id, size_id
    )
    if order_item:
        order = Order.objects.filter(user=user, status=status).first()
        if order:
            order.items.add(order_item)
            order.save()
        else:
            order = Order(user=user, status=status)
            if order:
                order.save()
                order.items.add(order_item)
                order.save()
            else:
                order_item.cancel()
                order_item = None

    return order_item


def is_the_order_item(
    menu_id, dish_id, type_id, flavor_id, size_id,
    item
):
    no_elems_ids = True

    if menu_id is not None:
        no_elems_ids = False
        elem = Menu.objects.filter(id=menu_id).first()
        if elem != item.menu.elem:
            return False

    if dish_id is not None:
        no_elems_ids = False
        elem = Dish.objects.filter(id=dish_id).first()
        if elem != item.dish.elem:
            return False

    if type_id is not None:
        no_elems_ids = False
        elem = Type.objects.filter(id=type_id).first()
        if elem != item.type.elem:
            return False

    if flavor_id is not None:
        no_elems_ids = False
        elem = Flavor.objects.filter(id=flavor_id).first()
        if elem != item.flavor.elem:
            return False

    if size_id is not None:
        no_elems_ids = False
        elem = Size.objects.filter(id=size_id).first()
        if elem != item.size.elem:
            return False

    if no_elems_ids:
        return False
    else:
        return True


def get_order_item(
        menu_id, dish_id, type_id, flavor_id, size_id,
        order
):
    items = order.items.all()
    founds = []
    for item in items:
        if is_the_order_item(
            menu_id, dish_id, type_id, flavor_id, size_id,
            item
        ):
            founds.append(item)

    if len(founds) > 0:
        order_item = founds[0]
    else:
        order_item = None

    return order_item


def get_order_item_by_user(
        menu_id, dish_id, type_id, flavor_id, size_id,
        user, status='InCart'
):
    order = Order.objects.filter(user=user, status=status).first()
    if order:
        order_item = get_order_item(
            menu_id, dish_id, type_id, flavor_id, size_id,
            order
        )
    else:
        order_item = None

    return order_item
