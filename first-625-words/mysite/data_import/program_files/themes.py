import os
import csv

from first625words.models import Theme

from . import helpers


def clear_data_all():
    d = Theme.objects.all()
    d.delete()


def get_data_all():
    d = Theme.objects.all()
    return d


def get_data(name):
    d = Theme.objects.filter(name=name)
    return d


def insert_data(data):
    d = Theme(name=data['name'], sort_number=data['sort_number'])
    d.save()


def import_data(path=None):
    target_path = build_target_path(path)
    if not os.path.isfile(target_path):
        return

    clear_data_all()

    with open(target_path) as file:
        rows = csv.reader(file)
        count = 0
        for row in rows:
            name = row[0]

            print(name, count)

            d = get_data(name)
            if not d:
                data = {
                    'name': name,
                    'sort_number': count
                }

                insert_data(data)

            count += 1


def build_target_path(path):
    target_base_name = 'themes.csv'

    target_path = helpers.build_target_path(target_base_name, path)

    return target_path
