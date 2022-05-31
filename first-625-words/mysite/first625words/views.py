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
    data_list = []

    for theme in themes:
        data = build_words_page_from_theme(theme, languages)

        data_list.append(data)

    counting = calc_words_page_counting(data_list)

    return {
        'counting': counting,
        'themes': data_list
    }


def calc_words_page_counting(data_list):
    count_max_images = 0
    count_max_languages = 0

    for data in data_list:
        counting = data['counting']

        count_images = counting['images']
        if count_images > count_max_images:
            count_max_images = count_images

        counts_phrases_for_languages = counting['phrases']
        count_languages = len(counts_phrases_for_languages)
        if count_languages > count_max_languages:
            count_max_languages = count_languages

    counts_max_phrases = [0] * count_max_languages

    for data in data_list:
        counting = data['counting']

        counts_phrases_for_languages = counting['phrases']
        count_languages = len(counts_phrases_for_languages)

        for i in range(count_languages):
            count_phrases = counts_phrases_for_languages[i]
            if count_phrases > counts_max_phrases[i]:
                counts_max_phrases[i] = count_phrases

    return {
        'images': count_max_images,
        'phrases': counts_max_phrases
    }    


def build_words_page_from_theme(theme, languages):
    data_list = []

    base_words = BaseWord.objects.filter(theme=theme).order_by('sort_number')

    for base_word in base_words:
        data = build_words_page_from_base_word(base_word, languages)

        data_list.append(data)

    counting = calc_words_page_counting(data_list)

    return {
        'theme': theme,
        'counting': counting,
        'themes': data_list
    }


def build_words_page_from_base_word(base_word, languages):
    words = Word.objects.filter(base_word=base_word)

    words_ordered = order_words_by_grouping_keys(words)

    data_list = build_words_page_from_words(words_ordered, languages)

    counting = calc_words_page_counting(data_list)

    return {
        'base_word': base_word,
        'counting': counting,
        'themes': data_list
    }


def order_words_by_grouping_keys(words):
    words_ordered = []

    for word in words:
        grouping_key = word.grouping_key

        key_number = calc_key_number_for_grouping_key(grouping_key)
        
        words_ordered.append({
            'word': word,
            'key_number': key_number
        })

    words_ordered.sort(key = lambda e: e['key_number'])

    return words_ordered


def calc_key_number_for_grouping_key(grouping_key):
    keys = grouping_key.split(GROUPING_KEYS_KEYS_SEPARATOR)

    key_number = 0
    for key in keys:
        key_number = key_number * GROUPING_KEYS_KEY_BASE_NUMBER + int(key) + 1

    return key_number


def build_words_page_from_words(words_ordered, languages):
    phrases_for_languages = get_phrases_for_words_ordered(words_ordered, languages)

    phrases_mergings = merge_phrases(words_ordered, phrases_for_languages)

    data_list = merge_images(words_ordered, phrases_mergings)

    return data_list


def get_phrases_for_words_ordered(words_ordered, languages):
    phrases_for_languages = []

    for language in languages:
        phrases_for_one_language = []

        for word_ordered in words_ordered:
            word = word_ordered['word']

            phrases = Phrase.objects.filter(word=word, language=language)

            phrases_for_one_language.append(phrases) 

        phrases_for_languages.append(phrases_for_one_language)

    return phrases_for_languages


def merge_phrases(words_ordered, phrases_for_languages):
    mergings = []

    indexes_for_languages = [0]  * len(phrases_for_languages)
    index_for_word = min(indexes_for_languages)
    
    while index_for_word < len(words_ordered):
        indexes_for_languages = get_next_phrases(
            phrases_for_languages, indexes_for_languages
            )

        index_for_word = min(indexes_for_languages)
        if index_for_word >= len(words_ordered):
            break

        merging = build_phrases_merging(
            words_ordered, phrases_for_languages,
            index_for_word, indexes_for_languages
            )

        mergings.append(merging)

    return mergings


def get_next_phrases(phrases_for_languages, indexes_for_languages):

    for i in range(len(phrases_for_languages)):
        phrases_for_one_language = phrases_for_languages[i]
        index_for_one_language = indexes_for_languages[i]

        while index_for_one_language < len(phrases_for_one_language):
            phrases = phrases_for_one_language[index_for_one_language]

            if phrases.count() > 0:
                break

            index_for_one_language += 1

        indexes_for_languages[i] = index_for_one_language

    return indexes_for_languages


def build_phrases_merging(
            words_ordered, phrases_for_languages,
            index_for_word, indexes_for_languages
            ):

    word_ordered = words_ordered[index_for_word]
    word = word_ordered['word']
    grouping = word.grouping
    grouping_key = word.grouping_key

    mergings_for_languages = []

    for i in range(len(phrases_for_languages)):
        phrases_for_one_language = phrases_for_languages[i]
        index_for_one_language = indexes_for_languages[i]
        merging_for_one_language = {}

        while index_for_one_language < len(phrases_for_one_language):
            phrases = phrases_for_one_language[index_for_one_language]

            word_ordered_for_one_language = words_ordered[index_for_one_language]
            word_for_one_language = word_ordered_for_one_language['word']
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
                    merging_for_one_language['word'] = word_ordered_for_one_language

                    break

            index_for_one_language += 1

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
    key_number1 = %= key_number1

    key_number2 = calc_key_number_for_grouping_key(grouping_key2)
    key_number2 = %= key_number2

    if key_number1 == key_number2:
        return True
    else:
        return False





def merge_images(words_ordered, phrases_merged):
    pass
