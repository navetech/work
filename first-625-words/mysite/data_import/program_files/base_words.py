import os
import csv

from first625words.models import BaseWord

from . import themes
from . import helpers


def get_data(text=None, theme=None):
    if text is None:
        if theme is None:
            d = None
        else:
            d = BaseWord.objects.filter(theme=theme)
    elif theme is None:
        d = BaseWord.objects.filter(text=text)
    else:
        d = BaseWord.objects.filter(text=text, theme=theme)

    return d


def clear_data_all():
    d = BaseWord.objects.all()
    d.delete()


def clear_data(text=None, theme=None):
    d = get_data(text, theme)
    d.delete()


def insert_data(data):
    d = BaseWord(text=data['text'], theme=data['theme'], sort_number=data['sort_number'])
    d.save()


def import_data(path=None):
    themes_ = themes.get_data_all()

    for theme in themes_:
        import_data_by_theme_name(name=theme.name, path=path)


def build_target_path(theme, path):
    target_base_name = theme.name.lower() + '-base-words.csv'

    target_path = helpers.build_target_path(target_base_name, path)

    return target_path


def import_data_by_theme_name(name, path=None):
    theme = themes.get_data(name).first()
    if not theme:
        return

    target_path = build_target_path(theme, path)
    if not os.path.isfile(target_path):
        return

    clear_data(theme=theme)

    with open(target_path) as file:
        rows = csv.reader(file)
        count = theme.sort_number * 1000 + 0
        for row in rows:
            text = row[0]

            print(text, theme.name, count)

            d = get_data(text, theme)
            if not d:
                data = {
                    'text': text,
                    'theme': theme,
                    'sort_number': count
                }

                insert_data(data)

            count += 1


def import_data_animal(path=None):
    name = 'Animal'
    import_data_by_theme_name(name=name, path=path)


def import_data_transportation(path=None):
    name = 'Transportation'
    import_data_by_theme_name(name=name, path=path)
