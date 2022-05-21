import os
import csv

from first625words.models import Theme

from . import helpers

from .settings import SORT_NUMBER_DEFAULT
from .settings import THEME_NAME_COLUMN
from .settings import SORT_NUMBER_INC_DEFAULT
from .settings import DATA_FILE_NAME_THEMES


def get_data_all():
    return Theme.objects.all()


def get_data(name):
    return Theme.objects.filter(name=name)


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(name, sort_number):
    d = Theme(name=name, sort_number=sort_number)
    d.save()


def import_data(path=None):
    target_path = build_target_path(path=path)
    if not os.path.isfile(target_path):
        return

    clear_data_all()

    with open(target_path) as file:
        rows = csv.reader(file)

        count = SORT_NUMBER_DEFAULT
        
        for row in rows:
            name = row[THEME_NAME_COLUMN]

            print(name, count)

            d = get_data(name=name)

            if not d:
                insert_data(name=name, sort_number=count)

            count += SORT_NUMBER_INC_DEFAULT


def build_target_path(path):
    base_name = DATA_FILE_NAME_THEMES

    target_path = helpers.build_target_path(base_name=base_name, path=path)

    return target_path
