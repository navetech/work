import os
import csv

from first625words.models import Image

from . import helpers

from . import themes
from . import base_words
from . import words

from .settings import WORD_BASE_WORD_COLUMN
from .settings import WORD_BASE_WORD_HEADER
from .settings import WORD_GROUPING_COLUMN
from .settings import WORD_GROUPING_HEADER
from .settings import WORD_GROUPING_KEY_COLUMN
from .settings import WORD_GROUPING_KEY_HEADER

from .settings import WORD_IMAGE_COLUMN
from .settings import WORD_IMAGE_HEADER
from .settings import DATA_FILE_NAME_ENDING_WORDS_IMAGES


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

    base_word_prev = None
    word_prev = None

    with open(target_path) as file:
        rows = csv.reader(file)

        for row in rows:
            image_link = row[WORD_IMAGE_COLUMN]
            if not image_link or image_link == WORD_IMAGE_HEADER:
                base_word_prev = None
                return


            base_word_text = row[WORD_BASE_WORD_COLUMN]
            if base_word_text == WORD_BASE_WORD_HEADER:
                base_word_prev = None
                return

            if base_word_text:
                base_word = base_words.get_data(text=base_word_text, theme=theme).first()
                if not base_word:
                    base_word_prev = None
                    return

            elif not base_word_prev:
                return
            else:
                base_word = base_word_prev

            base_word_prev = base_word

            grouping = row[WORD_GROUPING_COLUMN]
            if grouping == WORD_GROUPING_HEADER:
                base_word_prev = None
                return

            grouping_key = row[WORD_GROUPING_KEY_COLUMN]
            if grouping_key == WORD_GROUPING_KEY_HEADER:
                base_word_prev = None
                return

            if grouping_key and not grouping:
                base_word_prev = None
                return

            if not base_word_text and not grouping and not grouping_key:
                if word_prev:
                    word = word_prev
                else:
                    base_word_prev = None
                    return
            else:
                word = get_data(
                    base_word=base_word,
                    grouping=grouping, grouping_key=grouping_key
                    ).first()

            if not word:
                word = words.insert_data(
                    base_word=base_word,
                    grouping=grouping, grouping_key=grouping_key
                    )

            word_prev = word

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
