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
    ordered_word_phrases_for_languages = get_phrases_for_ordered_words(ordered_words, languages)

    phrases_mergings = merge_phrases(ordered_words, ordered_word_phrases_for_languages)

    mergings = merge_images(ordered_words, phrases_mergings)

    rows = []
    for merging in mergings:
        row = build_row_from_merging(merging)
        rows.append(row)

    return rows


def get_phrases_for_ordered_words(ordered_words, languages):
    phrases_for_languages = []

    for language in languages:
        phrases_for_one_language = []

        for ordered_word in ordered_words:
            word = ordered_word['word']

            phrases = Phrase.objects.filter(word=word, language=language)

            phrases_for_one_language.append(phrases) 

        phrases_for_languages.append(phrases_for_one_language)

    return phrases_for_languages


def merge_phrases(ordered_words, ordered_word_phrases_for_languages):
    mergings = []

    word_indexes_for_languages = [0]  * len(ordered_word_phrases_for_languages)
    word_index = min(word_indexes_for_languages)
    
    while word_index < len(ordered_words):
        word_indexes_for_languages = get_next_phrases(
            ordered_word_phrases_for_languages, word_indexes_for_languages
            )

        word_index = min(word_indexes_for_languages)
        if word_index >= len(ordered_words):
            break

        merging = build_phrases_merging(
            ordered_words, ordered_word_phrases_for_languages,
            word_index, word_indexes_for_languages
            )

        mergings.append(merging)

    return mergings


def get_next_phrases(ordered_word_phrases_for_languages, word_indexes_for_languages):
    for language_index in range(len(ordered_word_phrases_for_languages)):
        ordered_word_phrases_for_one_language = ordered_word_phrases_for_languages[language_index]
        word_index_for_one_language = word_indexes_for_languages[language_index]

        while word_index_for_one_language < len(ordered_word_phrases_for_one_language):
            phrases = ordered_word_phrases_for_one_language[word_index_for_one_language]

            if phrases.count() > 0:
                break

            word_index_for_one_language += 1

        word_indexes_for_languages[i] = word_index_for_one_language

    return word_indexes_for_languages


def build_phrases_merging(
        ordered_words, ordered_word_phrases_for_languages,
        word_index, word_indexes_for_languages
        ):

    ordered_word = ordered_words[word_index]
    word = ordered_word['word']
    grouping = word.grouping
    grouping_key = word.grouping_key

    mergings_for_languages = []

    for i in range(len(ordered_word_phrases_for_languages)):
        ordered_word_phrases_for_one_language = ordered_word_phrases_for_languages[i]
        word_index_for_one_language = word_indexes_for_languages[i]

        merging_for_one_language = {}

        while word_index_for_one_language < len(ordered_word_phrases_for_one_language):
            phrases = ordered_word_phrases_for_one_language[word_index_for_one_language]

            ordered_word_for_one_language = ordered_words[word_index_for_one_language]
            word_for_one_language = ordered_word_for_one_language['word']
            grouping_for_one_language = word_for_one_language.grouping
            grouping_key_for_one_language = word_for_one_language.grouping_key

            groupings_equivalent = are_groupings_equivalent(
                grouping, grouping_for_one_language, reverse=True
            )

            if groupings_equivalent:
                grouping_keys_equivalent = are_grouping_keys_equivalent(
                    grouping_key, grouping_key_for_one_language
                )

                if grouping_keys_equivalent:
                    merging_for_one_language['phrases'] = phrases
                    merging_for_one_language['word'] = word_for_one_language

                    break

            word_index_for_one_language += 1

        mergings_for_languages.append(merging_for_one_language)

    return {
        'for_languages': mergings_for_languages
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

    for i in range(len(groups1)):
        if groups1[i] != groups2[i]:
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

            merging_for_languages = merging['for_languages']
            for merging_for_one_language in merging_for_languages:
                word_for_one_language = merging_for_one_language['word']
                grouping_for_one_language = word_for_one_language.grouping

                groupings_equivalent = are_groupings_equivalent(
                    grouping, grouping_for_one_language, reverse=False
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

    phrases_for_languages = []
    for merging_for_one_language in merging['for_languages']:
        phrases_for_one_language = merging_for_one_language['phrases']

        phrases_for_languages.append(phrases_for_one_language)

    row['phrases_for_languages'] = phrases_for_languages

    return row


def calc_rows_counting(rows):
    counting = {}

    images_and_languages_counts = calc_images_and_languages_counts(rows)
    images_count = images_and_languages_counts['images']
    languages_count = images_and_languages_counts['languages']

    counting['images'] = images_count
    counting['languages'] = languages_count

    languages_countings = []
    for language_index in range(languages_count):
        one_language_counting = calc_one_language_counting(rows, language_index)
        languages_countings.append(one_language_counting)

    counting['for_languages'] = languages_countings

    return counting


def calc_images_and_languages_counts(rows):
    counts = {}

    images_count_max = 0
    languages_count_max = 0

    for row in rows:
        images_count = len(row['images'])
        images_count_max = max(images_count_max, images_count)

        languages_count = len(row['phrases_for_languages'])
        languages_count_max = max(languages_count_max, languages_count)

    counts['images'] = images_count_max
    counts['languages'] = languages_count_max

    return counts


def calc_one_language_counting(rows, language_index):
    counting = {}

    phrases_count  = calc_phrases_count(rows, language_index)

    counting['phrases'] = phrases_count

    phrases_countings = []
    for phrase_index in range(phrases_count):
        one_phrase_counting = calc_one_phrase_counting(rows, language_index, phrase_index)
        phrases_countings.append(one_phrase_counting)

    counting['for_phrases'] = phrases_countings

    return counting


def calc_phrases_count(rows, language_index):
    phrases_count_max = 0

    for row in rows:
        languages_count = len(row['phrases_for_languages'])

        if language_index < languages_count:
            phrases = row['phrases_for_languages'][language_index]

            phrases_count = len(phrases)
            phrases_count_max = max(phrases_count_max, phrases_count)

    return phrases_count_max


def calc_one_phrase_counting(rows, language_index, phrase_index):
    counting = {}

    pronunciations_count  = calc_pronunciations_count(rows, language_index, phrase_index)

    counting['pronunciations'] = pronunciations_count

    return counting


def calc_pronunciations_count(rows, language_index, phrase_index):
    pronunciations_count_max = 0

    for row in rows:
        languages_count = len(row['phrases_for_languages'])

        if language_index < languages_count:
            phrases = row['phrases_for_languages'][language_index]
            phrases_count = len(phrases)

            if phrase_index < phrases_count:
                phrase = phrases[phrase_index]

                pronunciations = phrase.pronunciations.all()

                pronunciations_count = len(pronunciations)
                pronunciations_count_max = max(pronunciations_count_max, pronunciations_count)

    return pronunciations_count_max
