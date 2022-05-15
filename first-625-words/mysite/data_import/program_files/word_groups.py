import os
import csv

from first625words.models import WordGroup

from . import helpers

from .settings import WORD_GROUP_NAME_COLUMN
from .settings import WORD_GROUP_NAME_HEADER
from .settings import WORD_GROUP_GROUPING_KEY_COLUMN
from .settings import WORD_GROUP_GROUPING_KEY_HEADER
from .settings import DATA_FILE_NAME_WORD_GROUPS


def clear_data_all():
    d = WordGroup.objects.all()
    d.delete()


def get_data_all():
    d = WordGroup.objects.all()
    return d


def get_data(name):
    d = WordGroup.objects.filter(name=name)
    return d


def insert_data(name, grouping_key):
    d = WordGroup(name=name, grouping_key=grouping_key)
    d.save()


def import_data(path=None):
    target_path = build_target_path(path=path)
    if not os.path.isfile(target_path):
        return

    clear_data_all()

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            if not row:
                continue
            
            name = row[WORD_GROUP_NAME_COLUMN]
            if not name or name == WORD_GROUP_NAME_HEADER:
                continue

            grouping_key = row[WORD_GROUP_GROUPING_KEY_COLUMN]
            if grouping_key == WORD_GROUP_GROUPING_KEY_HEADER:
                continue

            print(name, grouping_key)

            d = get_data(name=name)

            if not d:
                insert_data(name=name, grouping_key=grouping_key)


def build_target_path(path):
    base_name = DATA_FILE_NAME_WORD_GROUPS

    target_path = helpers.build_target_path(base_name=base_name, path=path)

    return target_path
