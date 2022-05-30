from django.shortcuts import render

# from django.http import HttpResponse

from first625words.models import Theme
from first625words.models import BaseWord
from first625words.models import Word
from first625words.models import Language
from first625words.models import Phrase

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

        keys = grouping_key.split('GROUPING_KEYS_KEYS_SEPARATOR')

        key_number = calc_key_number_for_grouping_keys(keys)
        
        words_ordered.append({
            'word': word,
            'key_number': key_number
        })

    words_ordered.sort(key = lambda e: e['key_number'])

    return words_ordered


def calc_key_number_for_grouping_keys(keys):
    key_number = 0
    for key in keys:
        key_number = key_number * GROUPING_KEYS_KEY_BASE_NUMBER + int(key) + 1

    return key_number


def build_words_page_from_words(words_ordered, languages):
    phrases_for_languages = get_phrases_for_words_ordered(words_ordered, languages)

    phrases_merged = merge_phrases(words_ordered, phrases_for_languages)

    data_list = merge_images(words_ordered, phrases_merged)

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


def merge_phrases(words_ordered, phrases):
    phrases_merged_list = []

    index_for_word = 0

    indexes_for_languages = []
    for language in range(len(phrases)):
        indexes_for_languages[language] = 0

    indexes = {}
    indexes['word'] = index_for_word
    indexes['languages'] = indexes_for_languages

    while index_for_word < len(words_ordered):
        indexes = get_next_word_with_phrases(words_ordered, phrases, indexes)

        index_for_word = indexes['word']
        if index_for_word >= len(words_ordered):
            break

        phrases_merged = build_phrases_merged(words_ordered, phrases, indexes)

        phrases_merged_list.append(phrases_merged)

    return phrases_merged_list


def get_next_word_with_phrases(words_ordered, phrases, indexes):
    indexes_ret = indexes

    index_for_word = indexes_ret['word']
    indexes_for_languages = indexes_ret['languages']

    while index_for_word < len(words_ordered):

        for language in range(len(phrases)):
            phrases_for_language = phrases[language]
            index_for_language = indexes_for_languages[language]
            found[language] = False
            found = False

            while index_for_language < len(phrases_for_language):

                for phrases_for_word in phrases_for_language>:
                    if phrases_for_word.count() > 0:
                        found = True
                        break

                if found:
                    break
                else:
                    index_for_language += 1

            indexes_for_languages[language] = index_for_language
            found[language] = found

        found = True
        for language in range(len(phrases)):
            if not found[language]:
                found = False
                break

        if found:
            break
        else:
            index_for_word += 1

    indexes_ret['word'] = index_for_word
    indexes_ret['languages'] = indexes_for_languages

    return indexes_ret



def merge_images(words_ordered, phrases_merged):

