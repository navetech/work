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

        dict['full_name'] = self.name.words

        if container_dict:
            dict['container'] = container_dict

            if 'full_name' in container_dict:
                dict['full_name'] += (
                    ' ' + container_dict['full_name']
                )

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

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['elem'] = menu_elem_to_dict(
            dict, self.elem, **settings
        )

        return dict


class OrderAddingFlavor(models.Model):
    elem = models.ForeignKey(
        AddingFlavor, blank=True, null=True, on_delete=models.CASCADE,
        related_name='elem_OrderAddigFlavor_related'
    )

    size = models.ForeignKey(
        OrderSize, blank=True, null=True, on_delete=models.CASCADE,
        related_name='size_OrderAddingFlavor_related'
    )

    selected = models.BooleanField(default=False)

    def cancel(self):
        if self.size:
            self.size.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['elem'] = menu_elem_to_dict(
            dict, self.elem, **settings
        )

        dict['size'] = to_dict(self.size, **settings)

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

    def cancel(self):
        for flavor in self.flavors.all():
            flavor.cancel()

        self.delete()

    def __str__(self):
        return (
            f'{self.elem}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['elem'] = menu_elem_to_dict(
            dict, self.elem, **settings
        )

        dict['flavors'] = to_dict_list(self.flavors, **settings)

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

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['elem'] = menu_elem_to_dict(
            dict, self.elem, **settings
        )

        dict['addings'] = to_dict_list(self.addings, **settings)

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

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['elem'] = menu_elem_to_dict(
            dict, self.elem, **settings
        )

        dict['addings'] = to_dict_list(self.addings, **settings)

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
            f'{self.proprio}, '
        )

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['elem'] = menu_elem_to_dict(
            dict, self.proprio, **settings
        )

        dict['addings'] = to_dict_list(self.addings, **settings)

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

    def to_dict(self, **settings):
        dict = {}

        dict['id'] = self.id

        dict['elem'] = menu_elem_to_dict(
            dict, self.elem, **settings
        )

        dict['addings'] = to_dict_list(self.addings, **settings)

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


def create_order_adding_flavor(adding_flavor, selected):
    order_elem = OrderAddingFlavor(elem=adding_flavor, selected=selected)
    if order_elem:
        order_elem.save()

    return order_elem


def create_order_adding(adding):
    order_elem = OrderAdding(elem=adding)
    if order_elem:
        order_elem.save()

        flavors = adding.flavors_set.flavors.all()
        for flavor in flavors:
            if flavor.special and adding.only_special_flavors:
                selected = True
            else:
                selected = False
                
            order_adding_flavor = create_order_adding_flavor(flavor, selected)
            order_elem.flavors.add(order_adding_flavor)
            order_elem.save()

    return order_elem


def create_order_menu(menu_id):
    print('create_order_menu', menu_id)
    elem = Menu.objects.filter(id=menu_id).first()
    print(elem)
    if elem:
        print(elem)
        order_elem = OrderMenu(elem=elem)
        print(order_elem)
        if order_elem:
            print('xxx')
            print(order_elem)
            order_elem.save()
            print('all')
            print(elem.addings.all())
            for adding in elem.addings.all():
                print('adding')
                print(adding)
                order_adding = create_order_adding(adding)
                order_elem.addings.add(order_adding)
                order_elem.save()
    else:
        order_elem = None

    return order_elem


def create_order_dish(dish_id):
    elem = Dish.objects.filter(id=dish_id).first()
    if elem:
        order_elem = OrderDish(elem=elem)
        if order_elem:
            order_elem.save()
            for adding in elem.addings.all():
                order_adding = create_order_adding(adding)
                order_elem.addings.add(order_adding)
                order_elem.save()
    else:
        order_elem = None

    order_elem = None

    return order_elem


def create_order_type(type_id):
    elem = Type.objects.filter(id=type_id).first()
    if elem:
        order_elem = OrderType(elem=elem)
        if order_elem:
            order_elem.save()
            for adding in elem.addings.all():
                order_adding = create_order_adding(adding)
                order_elem.addings.add(order_adding)
                order_elem.save()
    else:
        order_elem = None

    return order_elem


def create_order_flavor(flavor_id):
    elem = Flavor.objects.filter(id=flavor_id).first()
    if elem:
        order_elem = OrderFlavor(elem=elem)
        if order_elem:
            order_elem.save()
            for adding in elem.addings.all():
                order_adding = create_order_adding(adding)
                order_elem.addings.add(order_adding)
                order_elem.save()
    else:
        order_elem = None

    return order_elem


def create_order_elem(elem_id, elem_class, order_elem_class):
    elem = elem_class.objects.filter(id=elem_id).first()
    print(elem)
    if elem:
        print('elem')
        print(elem)
        order_elem = order_elem_class(elem=elem)
        print(order_elem)
        if order_elem:
            print('order_elem')
            print(order_elem)
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
    print('create_order_item')
    menu = create_order_elem(menu_id, Menu, OrderMenu)
#    menu = create_order_menu(menu_id)
    print('menu')
    print(menu)
#    dish = create_order_dish(dish_id)
    dish = create_order_elem(dish_id, Dish, OrderDish)
#    type = create_order_type(type_id)
    type = create_order_elem(type_id, Type, OrderType)
#    flavor = create_order_flavor(flavor_id)
    flavor = create_order_elem(flavor_id, Flavor, OrderFlavor)
    size = create_order_size(size_id)

    if menu or dish or type or flavor or size:
        order_item = OrderItem(
            count=1,
            menu=menu, dish=dish, type=type,
            flavor=flavor, size=size
        )
        print(order_item)
        order_item.save()
        print('order_item')
        print(order_item)
    else:
        order_item = None

    return order_item


def create_order_item_for_user(
        menu_id, dish_id, type_id, flavor_id, size_id,
        user, status='InCart'
):
    print('create_order_item_for_user')
    order_item = create_order_item(
        menu_id, dish_id, type_id, flavor_id, size_id
    )
    if order_item:
        print('output create_order_item_for_user')
        print(order_item)
        order = Order.objects.filter(user=user, status=status).first()
        print(order)
        if order:
            print('order')
            order.items.add(order_item)
            order.save()
            print(order)
        else:
            print('no order')
            order = Order(user=user, status=status)
            if order:
                order.save()
                print('create order')
                order.items.add(order_item)
                order.save()
                print(order)
            else:
                print('cancel order_item')
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
    print('items')
    print(items)
    founds = []
    for item in items:
        print('item')
        print(item)
        if is_the_order_item(
            menu_id, dish_id, type_id, flavor_id, size_id,
            item
        ):
            founds.append(item)

    print('founds')    
    print(len(founds))

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
    print('order')
    print(order)
    if order:
        order_item = get_order_item(
            menu_id, dish_id, type_id, flavor_id, size_id,
            order
        )
    else:
        order_item = None

    return order_item


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
