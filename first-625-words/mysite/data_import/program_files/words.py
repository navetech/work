import os
import csv

from first625words.models import Word

from . import helpers

from .settings import WORD_BASE_WORD_COLUMN
from .settings import WORD_BASE_WORD_HEADER
from .settings import WORD_GROUPING_COLUMN
from .settings import WORD_GROUPING_HEADER
from .settings import WORD_GROUPING_KEY_COLUMN
from .settings import WORD_GROUPING_KEY_HEADER


def get_data_all():
    return Word.objects.all()


def get_data(base_word=None, grouping=None, grouping_key=None):
    if base_word is None:
        d = None
    elif grouping is None:
        d = Word.objects.filter(base_word=base_word)
    elif grouping_key is None:
        d = Word.objects.filter(
            base_word=base_word, grouping=grouping
            )
    else:
        d = Word.objects.filter(
            base_word=base_word,
            grouping=grouping, grouping_key=grouping_key
            )

    return d


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(base_word, grouping, grouping_key):
    d = Word(
        base_word=base_word,
        grouping=grouping, grouping_key=grouping_key
        )

    d.save()
