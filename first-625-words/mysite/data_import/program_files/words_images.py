import os
import csv

from first625words.models import Image

from . import helpers

from . import themes
from . import base_words
from . import words

from .settings import DATA_FILE_NAME_ENDING_WORDS_IMAGES
from .settings import IMAGE_BASE_WORD_COLUMN
from .settings import IMAGE_BASE_WORD_HEADER
from .settings import IMAGE_GROUPING_COLUMN
from .settings import IMAGE_GROUPING_HEADER
from .settings import IMAGE_GROUPING_KEY_COLUMN
from .settings import IMAGE_GROUPING_KEY_HEADER
from .settings import IMAGE_COLUMN
from .settings import IMAGE_HEADER


def get_data_all():
    return Image.objects.all()


def get_data(link):
    return Image.objects.filter(link=link)


def clear_data_all():
    d = get_data_all()
    d.delete()


def clear_data_by_theme(theme=None):
    base_words_ = base_words.get_data(theme=theme)

    for base_word in base_words_:
        words_ = words.get_data(base_word=base_word)

        for word in words_:
            images = word.images.all()

            for image in images:
                word.images.remove(image)
                image.delete()


def insert_data(link):
    d = Image(link=link)
    d.save()


def import_data(path=None):
    themes_ = themes.get_data_all()

    for theme in themes_:
        import_data_by_theme(theme=theme, path=path)


def import_data_by_theme(theme, path=None):
    target_path = build_target_path(theme=theme, path=path)
    if not os.path.isfile(target_path):
        return

    clear_data_by_theme(theme=theme)

    word_prev = None

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            image_link = row[IMAGE_COLUMN]
            if image_link == IMAGE_HEADER:
                word_prev = None
                return

            if not image_link:
                word_prev = None
                return

            row_column = {
                'base_word': IMAGE_BASE_WORD_COLUMN,
                'grouping': IMAGE_GROUPING_COLUMN,
                'grouping_key': IMAGE_GROUPING_KEY_COLUMN
            }

            column_header = {
                'base_word': IMAGE_BASE_WORD_HEADER,
                'grouping': IMAGE_GROUPING_HEADER,
                'grouping_key': IMAGE_GROUPING_KEY_HEADER
            }

            word = words.get_data_from_row(
                row=row,
                row_column=row_column, column_header=column_header,
                theme=theme, word_prev=word_prev
                )

            word_prev = word

            if word is None:
                return

            word_images = word.images.all()

            image = get_data(link=image_link).first()
            if not image:
                image = insert_data(link=image_link)

            if image in word_images:
                return
            
            word_images.add(image)


def build_target_path(theme, path):
    base_name = f'{theme.name.lower()}{DATA_FILE_NAME_ENDING_WORDS_IMAGES}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)

    return target_path
