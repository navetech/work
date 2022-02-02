from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'orders'

"""
from django.apps import AppConfig


from django.db.models.signals import m2m_changed


def types_changed(sender, **kwargs):
    instance = kwargs['instance']
    objects = instance.types
    objects_count = instance.types_count

    ret = objects_count_changed(objects, objects_count, sender, **kwargs)

    if ret['changed']:
        instance.types_count = ret['objects_count']
        if instance.types_count:
            instance.types_count.save()
        instance.save()


def flavors_changed(sender, **kwargs):
    instance = kwargs['instance']
    objects = instance.flavors
    objects_count = instance.flavors_count

    ret = objects_count_changed(objects, objects_count, sender, **kwargs)

    if ret['changed']:
        instance.flavors_count = ret['objects_count']
        if instance.flavors_count:
            instance.flavors_count.save()
        instance.save()


def sizes_changed(sender, **kwargs):
    instance = kwargs['instance']
    objects = instance.sizes
    objects_count = instance.sizes_count

    ret = objects_count_changed(objects, objects_count, sender, **kwargs)

    if ret['changed']:
        instance.sizes_count = ret['objects_count']
        if instance.sizes_count:
            instance.sizes_count.save()
        instance.save()


def addings_changed(sender, **kwargs):
    instance = kwargs['instance']
    objects = instance.addings
    objects_count = instance.addings_count

    ret = objects_count_changed(objects, objects_count, sender, **kwargs)

    if ret['changed']:
        instance.addings_count = ret['objects_count']
        if instance.addings_count:
            instance.addings_count.save()
        instance.save()


def objects_count_changed(objects, objects_count, sender, **kwargs):
    from .models import CountLimit

    changed = False

    if kwargs['reverse']:
        pass
    else:
        action = kwargs['action']
        if action == 'post_add':
            if not objects_count:
                objects_count = CountLimit.objects.filter(min=0, max=-1).first()
                if not objects_count:
                    objects_count = CountLimit(min=0, max=-1)
                changed = True
        elif action == 'post_remove':
            if objects.count() < 1:
                if objects_count:
                    objects_count = None
                    changed = True

    return {
        'changed': changed,
        'objects_count': objects_count,
    }


class OrdersConfig(AppConfig):
    name = 'orders'


    def ready(self):
        from .models import Dish
        from .models import Type
        from .models import Flavor
        from .models import Adding

        m2m_changed.connect(types_changed, sender=Dish.types.through)
        m2m_changed.connect(flavors_changed, sender=Dish.flavors.through)
        m2m_changed.connect(sizes_changed, sender=Dish.sizes.through)
        m2m_changed.connect(addings_changed, sender=Dish.addings.through)

        m2m_changed.connect(flavors_changed, sender=Type.flavors.through)
        m2m_changed.connect(sizes_changed, sender=Type.sizes.through)
        m2m_changed.connect(addings_changed, sender=Type.addings.through)

        m2m_changed.connect(sizes_changed, sender=Flavor.sizes.through)
        m2m_changed.connect(addings_changed, sender=Flavor.addings.through)

        m2m_changed.connect(flavors_changed, sender=Adding.flavors.through)
        m2m_changed.connect(sizes_changed, sender=Adding.sizes.through)
"""
