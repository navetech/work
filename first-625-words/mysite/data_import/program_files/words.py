import os
import csv

from first625words.models import Word

from . import helpers

from . import base_words


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


def get_data_from_row(
    row, row_column, column_header,
    theme=None, word_prev=None
    ):

    if word_prev:
        base_word_prev = word_prev.base_word
    else:
        base_word_prev = None

    base_word = base_words.get_data_from_row(
        row=row,
        row_column=row_column['base_word'],
        column_header=column_header['base_word'],
        theme=theme, base_word_prev=base_word_prev
        )

    if base_word is None:
        return None

    grouping = helpers.get_cell_data_from_row(
        row=row,
        row_column=row_column['grouping'],
        column_header=column_header['grouping'],
        )

    if grouping is None:
        return None

    grouping_key = helpers.get_cell_data_from_row(
        row=row,
        row_column=row_column['grouping_key'],
        column_header=column_header['grouping_key'],
        )

    if grouping_key is None:
        return None

    if grouping_key and not grouping:
        return

    word = get_data(
        base_word=base_word,
        grouping=grouping, grouping_key=grouping_key
        ).first()

    if not word:
        if xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    else:
        if word_prev:
            word = word_prev
        else:
            base_word_prev = None
            return

    if not word:
        word = words.insert_data(
            base_word=base_word,
            grouping=grouping, grouping_key=grouping_key
            )

    return word

