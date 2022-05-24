import csv

from first625words.models import Theme

from . import themes
from . import base_words
from . import images
from . import words
from . import languages
from . import spellings
from . import phrases


def clear_data_all():
    themes.clear_data_all()
    base_words.clear_data_all()
    images.clear_data_all()
    words.clear_data_all()
    languages.clear_data_all()
    spellings.clear_data_all()
    phrases.clear_data_all()


def import_data(path=None):
    print()

    clear_data_all()

    themes.import_data(path)
    base_words.import_data(path)
    images.import_data_for_words(path)
    languages.import_data(path)
    spellings.import_data_for_words(path)

    print()

