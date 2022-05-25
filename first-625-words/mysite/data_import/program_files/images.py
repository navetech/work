import csv

from first625words.models import Image
from first625words.models import Theme
from first625words.models import BaseWord
from first625words.models import Word

from . import helpers

from . import words

from .settings import DATA_FILES_EXTENSION
from .settings import DATA_FILES_FILE_NAME_ROOTS_SEPARATOR

from .settings import WORDS_FILE_NAME_ROOT

from .settings import IMAGES_FILE_NAME_ROOT
from .settings import IMAGE_BASE_WORD_COLUMN
from .settings import IMAGE_BASE_WORD_HEADER
from .settings import IMAGE_GROUPING_COLUMN
from .settings import IMAGE_GROUPING_HEADER
from .settings import IMAGE_GROUPING_KEY_COLUMN
from .settings import IMAGE_GROUPING_KEY_HEADER
from .settings import IMAGE_COLUMN
from .settings import IMAGE_HEADER


def clear_data_all():
    d = Image.objects.all()
    d.delete()


def clear_data_for_words_by_theme(theme):
    base_words_ = BaseWord.objects.filter(theme=theme)

    for base_word in base_words_:
        words_ = Word.objects.filter(base_word=base_word)

        for word in words_:
            images = word.images.all()

            for image in images:
                word.images.remove(image)
                image.delete()


def import_data_for_words(path=None):
    print()

    themes_ = Theme.objects.all()

    for theme in themes_:
        import_data_for_words_by_theme(theme=theme, path=path)


def import_data_for_words_by_theme(theme, path=None):
    base_name = f'{IMAGES_FILE_NAME_ROOT}'
    base_name += f'{DATA_FILES_FILE_NAME_ROOTS_SEPARATOR}'
    base_name += f'{WORDS_FILE_NAME_ROOT}'
    base_name += f'{DATA_FILES_FILE_NAME_ROOTS_SEPARATOR}'
    base_name += f'{theme.name.lower()}'
    base_name += f'{DATA_FILES_EXTENSION}'

    target_path = helpers.build_target_path(base_name=base_name, path=path)
    if target_path is None:
        return

    # clear_data_for_words_by_theme(theme=theme)

    word_prev = None

    print()

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            image_link = helpers.get_cell_from_row(
                row=row, column=IMAGE_COLUMN, column_header=IMAGE_HEADER
            )

            if (
                image_link is None or
                not str(image_link) or str(image_link).isspace()
            ):
                word_prev = None
                continue

            column = {
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
                column=column, column_header=column_header,
                theme=theme, word_prev=word_prev
                )

            word_prev = word

            if not word:
                continue

            image = Image.objects.filter(link=image_link).first()
            if not image:
                image = Image(link=image_link)
                image.save()

                print()
                print('### IMAGE CREATED ###')

            word_images = word.images.all()
            if image not in word_images:
                word.images.add(image)

                print()
                print('### IMAGE ADDED TO WORD ###')

            print()
            print(
                word.base_word.text, word.grouping,
                word.grouping_key, image.link
                )

    print()
