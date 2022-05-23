import csv

from first625words.models import Language

from . import helpers

from .settings import LANGUAGES_FILE_NAME
from .settings import LANGUAGE_COLUMN
from .settings import LANGUAGE_HEADER


def get_data_all():
    return Language.objects.all()


def get_data(name):
    return Language.objects.filter(name=name)


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(name):
    d = Language(name=name)
    d.save()

    return d


def import_data(path=None):
    print()


    base_name = LANGUAGES_FILE_NAME

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    clear_data_all()

    print()

    with open(target_path) as file:
        rows = csv.reader(file)
        
        for row in rows:
            name = helpers.get_cell_from_row(
                row=row, column=LANGUAGE_COLUMN, column_header=LANGUAGE_HEADER
            )

            if name is None or not str(name) or str(name).isspace():
                continue

            language = get_data(name=name)
            if not language:
                language = insert_data(name=name)

            print()
            print(language.name)

    print()

