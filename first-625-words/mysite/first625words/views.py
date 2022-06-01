from django.shortcuts import render

# from django.http import HttpResponse

from first625words.models import Theme
from first625words.models import BaseWord
from first625words.models import Word
from first625words.models import Language
from first625words.models import Phrase

from .settings import GROUPING_GROUPS_SEPARATOR
from .settings import GROUPING_KEYS_KEYS_SEPARATOR
from .settings import GROUPING_KEYS_KEY_BASE_NUMBER


# Create your views here.

def index(request):
    themes = Theme.objects.all()

    languages = Language.objects.all()

    data = build_words_page(themes, languages)

    context = {
        'data': data,
    }

    return render(request, 'first625words/words.html', context)

    # return HttpResponse("Hello, world. You're at the first625words index.")


def build_words_page(themes, languages):
    data = {}

    themes_data_list = []
    for theme in themes:
        theme_data = build_words_page_from_theme(theme, languages)

        themes_data_list.append(theme_data)

    counting = calc_list_counting(themes_data_list)

    data['counting'] = counting
    data['for_themes'] = themes_data_list

    return data


def calc_list_counting(data_list):
    counting = {}

    images_and_languages_counts = calc_list_images_and_languages_counts(data_list)
    images_count = images_and_languages_counts['images']
    languages_count = images_and_languages_counts['languages']

    counting['images'] = images_count
    counting['languages'] = languages_count

    languages_countings = []
    for language_index in range(languages_count):
        one_language_counting = calc_list_one_language_counting(data_list, language_index)
        languages_countings.append(one_language_counting)

    counting['for_languages'] = languages_countings

    return counting


def calc_list_images_and_languages_counts(data_list):
    counts = {}

    images_count_max = 0
    languages_count_max = 0

    for data in data_list:
        counting = data['counting']

        images_count = counting['images']
        images_count_max = max(images_count_max, images_count)

        languages_count = counting['languages']
        languages_count_max = max(languages_count_max, languages_count)

    counts['images'] = images_count_max
    counts['languages'] = languages_count_max

    return counts


def calc_list_one_language_counting(data_list, language_index):
    counting = {}

    phrases_count  = calc_list_phrases_count(data_list, language_index)

    counting['phrases'] = phrases_count

    phrases_countings = []
    for phrase_index in range(phrases_count):
        one_phrase_counting = calc_list_one_phrase_counting(data_list, language_index, phrase_index)
        phrases_countings.append(one_phrase_counting)

    counting['for_phrases'] = phrases_countings

    return counting


def calc_list_phrases_count(data_list, language_index):
    phrases_count_max = 0

    for data in data_list:
        counting = data['counting']

        languages_count = len(counting['for_languages'])

        if language_index < languages_count:
            one_language_counting = counting['for_languages'][language_index]

            phrases_count = len(one_language_counting['phrases'])
            phrases_count_max = max(phrases_count_max, phrases_count)

    return phrases_count_max


def calc_list_one_phrase_counting(data_list, language_index, phrase_index):
    counting = {}

    pronunciations_count  = calc_list_pronunciations_count(data_list, language_index, phrase_index)

    counting['pronunciations'] = pronunciations_count

    return counting


def calc_list_pronunciations_count(data_list, language_index, phrase_index):
    pronunciations_count_max = 0

    for data in data_list:
        counting = data['counting']

        languages_count = len(counting['for_languages'])

        if language_index < languages_count:
            one_language_counting = counting['for_languages'][language_index]

            phrases_count = len(one_language_counting['phrases'])

            if phrase_index < phrases_count:
                one_phrase_counting = one_language_counting['for_phrases'][phrase_index]

                pronunciations_count = one_phrase_counting['pronunciations']
                pronunciations_count_max = max(pronunciations_count_max, pronunciations_count)

    return pronunciations_count_max


def build_words_page_from_theme(theme, languages):
    data = {}

    base_words = BaseWord.objects.filter(theme=theme).order_by('sort_number')

    base_words_data_list = []
    for base_word in base_words:
        base_word_data = build_words_page_from_base_word(base_word, languages)

        base_words_data_list.append(base_word_data)

    counting = calc_list_counting(base_words_data_list)

    data['theme'] = theme
    data['counting'] = counting
    data['for_base_words'] = base_words_data_list

    return data


def build_words_page_from_base_word(base_word, languages):
    data = {}

    words = Word.objects.filter(base_word=base_word)

    ordered_words = order_words_by_grouping_keys(words)

    rows = build_rows_from_words(ordered_words, languages)

    counting = calc_rows_counting(rows)

    data['base_word'] = base_word
    data['counting'] = counting
    data['rows'] = rows

    return data


def order_words_by_grouping_keys(words):
    ordered_words = []

    for word in words:
        grouping_key = word.grouping_key

        key_number = calc_key_number_for_grouping_key(grouping_key)
        
        ordered_words.append({
            'word': word,
            'key_number': key_number
        })

    ordered_words.sort(key = lambda e: e['key_number'])

    return ordered_words


def calc_key_number_for_grouping_key(grouping_key):
    keys = grouping_key.split(GROUPING_KEYS_KEYS_SEPARATOR)

    key_number = 0
    for key in keys:
        key_number = key_number * GROUPING_KEYS_KEY_BASE_NUMBER + int(key) + 1

    return key_number


def build_rows_from_words(ordered_words, languages):
    ordered_word_languages_phrases = get_phrases_for_ordered_words(ordered_words, languages)

    phrases_mergings = merge_phrases(ordered_words, ordered_word_languages_phrases)

    mergings = merge_images(ordered_words, phrases_mergings)

    rows = []
    for merging in mergings:
        row = build_row_from_merging(merging)
        rows.append(row)

    return rows


def get_phrases_for_ordered_words(ordered_words, languages):
    languages_phrases = []

    for language in languages:
        one_language_phrases = []

        for ordered_word in ordered_words:
            word = ordered_word['word']

            phrases = Phrase.objects.filter(word=word, language=language)

            one_language_phrases.append(phrases) 

        languages_phrases.append(one_language_phrases)

    return languages_phrases


def merge_phrases(ordered_words, ordered_word_languages_phrases):
    mergings = []

    ordered_word_languages_indexes = [0]  * len(ordered_word_languages_phrases)
    ordered_word_index = min(ordered_word_languages_indexes)
    
    while ordered_word_index < len(ordered_words):
        ordered_word_languages_indexes = get_next_phrases(
            ordered_word_languages_phrases, ordered_word_languages_indexes
            )

        ordered_word_index = min(ordered_word_languages_indexes)
        if ordered_word_index >= len(ordered_words):
            break

        merging = build_phrases_merging(
            ordered_words, ordered_word_languages_phrases,
            ordered_word_index, ordered_word_languages_indexes
            )

        mergings.append(merging)

    return mergings


def get_next_phrases(ordered_word_languages_phrases, ordered_word_languages_indexes):

    for language_index in range(len(ordered_word_languages_phrases)):
        ordered_word_one_language_phrases = ordered_word_languages_phrases[language_index]

        ordered_word_one_language_index = ordered_word_languages_indexes[language_index]

        while ordered_word_one_language_index < len(ordered_word_one_language_phrases):
            phrases = ordered_word_one_language_phrases[ordered_word_one_language_index]

            if phrases.count() > 0:
                break

            ordered_word_one_language_index += 1

        ordered_word_languages_indexes[i] = ordered_word_one_language_index

    return ordered_word_languages_indexes


def build_phrases_merging(
        ordered_words, ordered_word_languages_phrases,
        ordered_word_index, ordered_word_languages_indexes
        ):

    ordered_word = ordered_words[ordered_word_index]
    word = ordered_word['word']
    grouping = word.grouping
    grouping_key = word.grouping_key

    languages_mergings = []

    for language_index in range(len(ordered_word_languages_phrases)):
        ordered_word_one_language_phrases = ordered_word_languages_phrases[language_index]

        ordered_word_one_language_index = ordered_word_languages_indexes[language_index]

        one_language_merging = {}

        while ordered_word_one_language_index < len(ordered_word_one_language_phrases):
            phrases = ordered_word_one_language_phrases[ordered_word_one_language_index]

            one_language_ordered_word = ordered_words[ordered_word_one_language_index]

            one_language_word = one_language_ordered_word['word']

            one_language_grouping = one_language_word.grouping
            one_language_grouping_key = one_language_word.grouping_key

            groupings_equivalent = are_groupings_equivalent(
                grouping, one_language_grouping, reverse=True
            )

            if groupings_equivalent:
                grouping_keys_equivalent = are_grouping_keys_equivalent(
                    grouping_key, one_language_grouping_key
                )

                if grouping_keys_equivalent:
                    one_language_merging['phrases'] = phrases
                    one_language_merging['word'] = one_language_word

                    break

            ordered_word_one_language_index += 1

        languages_mergings.append(one_language_merging)

    return {
        'for_languages': languages_mergings
    }


def are_groupings_equivalent(grouping1, grouping2, reverse=False):
    if grouping1 == grouping2:
        return True
    elif is_grouping1_in_grouping2(grouping1, grouping2, reverse):
        return True
    elif is_grouping1_in_grouping2(grouping2, grouping1, reverse):
        return True
    else:
        return False
    

def is_grouping1_in_grouping2(grouping1, grouping2, reverse=False):
    groups1 = grouping1.split(GROUPING_GROUPS_SEPARATOR)
    groups2 = grouping2.split(GROUPING_GROUPS_SEPARATOR)

    if reverse:
        groups1.reverse()
        groups2.reverse()

    for group_index in range(len(groups1)):
        if groups1[group_index] != groups2[group_index]:
            return False
    
    return True


def are_grouping_keys_equivalent(grouping_key1, grouping_key2):
    if grouping_key1 == grouping_key2:
        return True

    key_number1 = calc_key_number_for_grouping_key(grouping_key1)
    key_number1 %= key_number1

    key_number2 = calc_key_number_for_grouping_key(grouping_key2)
    key_number2 %= key_number2

    if key_number1 == key_number2:
        return True
    else:
        return False


def merge_images(ordered_words, mergings):
    for ordered_word in ordered_words:
        word = ordered_word['word']

        images = word.images.all()
        if images.count() < 1:
            continue

        grouping = word.grouping

        images_merged = False

        for merging in mergings:
            merging['images'] = []

            languages_mergings = merging['for_languages']
            for one_language_merging in languages_mergings:
                one_language_word = one_language_merging['word']

                one_language_grouping = one_language_word.grouping

                groupings_equivalent = are_groupings_equivalent(
                    grouping, one_language_grouping, reverse=False
                )

                if groupings_equivalent and not images_merged:
                    merging['images'].append(images)
                    images_merged = True

                    break

            if images_merged:
                break

    return mergings


def build_row_from_merging(merging):
    row = {}

    row['images'] = merging['images']

    languages_phrases = []
    for one_language_merging in merging['for_languages']:
        one_language_phrases = one_language_merging['phrases']

        languages_phrases.append(one_language_phrases)

    row['languages_phrases'] = languages_phrases

    return row


def calc_rows_counting(rows):
    counting = {}

    images_and_languages_counts = calc_rows_images_and_languages_counts(rows)
    images_count = images_and_languages_counts['images']
    languages_count = images_and_languages_counts['languages']

    counting['images'] = images_count
    counting['languages'] = languages_count

    languages_countings = []
    for language_index in range(languages_count):
        one_language_counting = calc_rows_one_language_counting(rows, language_index)
        languages_countings.append(one_language_counting)

    counting['for_languages'] = languages_countings

    return counting


def calc_rows_images_and_languages_counts(rows):
    counts = {}

    images_count_max = 0
    languages_count_max = 0

    for row in rows:
        images_count = len(row['images'])
        images_count_max = max(images_count_max, images_count)

        languages_count = len(row['languages_phrases'])
        languages_count_max = max(languages_count_max, languages_count)

    counts['images'] = images_count_max
    counts['languages'] = languages_count_max

    return counts


def calc_rows_one_language_counting(rows, language_index):
    counting = {}

    phrases_count  = calc_rows_phrases_count(rows, language_index)

    counting['phrases'] = phrases_count

    phrases_countings = []
    for phrase_index in range(phrases_count):
        one_phrase_counting = calc_rows_one_phrase_counting(rows, language_index, phrase_index)
        phrases_countings.append(one_phrase_counting)

    counting['for_phrases'] = phrases_countings

    return counting


def calc_rows_phrases_count(rows, language_index):
    phrases_count_max = 0

    for row in rows:
        languages_count = len(row['languages_phrases'])

        if language_index < languages_count:
            phrases = row['phrases_for_languages'][language_index]

            phrases_count = len(phrases)
            phrases_count_max = max(phrases_count_max, phrases_count)

    return phrases_count_max


def calc_rows_one_phrase_counting(rows, language_index, phrase_index):
    counting = {}

    pronunciations_count  = calc_rows_pronunciations_count(rows, language_index, phrase_index)

    counting['pronunciations'] = pronunciations_count

    return counting


def calc_rows_pronunciations_count(rows, language_index, phrase_index):
    pronunciations_count_max = 0

    for row in rows:
        languages_count = len(row['languages_phrases'])

        if language_index < languages_count:
            phrases = row['phrases_for_languages'][language_index]
            phrases_count = len(phrases)

            if phrase_index < phrases_count:
                phrase = phrases[phrase_index]

                pronunciations = phrase.pronunciations.all()

                pronunciations_count = len(pronunciations)
                pronunciations_count_max = max(pronunciations_count_max, pronunciations_count)

    return pronunciations_count_max
