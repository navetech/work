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

    rows = []

    for theme in themes:
        base_words = BaseWord.objects.filter(theme=theme)

        for base_word in base_words:
            words = Word.objects.filter(base_word=base_word)

            words_ordered = order_words_by_grouping_keys(words)

            phrases = get_phrases_for_words_ordered(words_ordered, languages)

            first625words = merge_phrases_and_images(words_ordered, phrases)

        row = {
            'theme': theme,
            'first625words': first625words
        }

        rows.append(row)

    context = {
        'rows': rows,
    }

    return render(request, 'first625words/first625words.html', context)

    # return HttpResponse("Hello, world. You're at the first625words index.")



def order_words_by_grouping_keys(words):
    words_ordered = []

    for word in words:
        grouping_key = word.grouping_key

        keys = grouping_key.split('GROUPING_KEYS_KEYS_SEPARATOR')

        sort_number = calc_sort_number_for_grouping_keys(keys)
        
        words_ordered.append({
            'word': word,
            'sort_number': sort_number
        })

    words_ordered.sort(key = lambda e: e['sort_number'])

    return words_ordered


def calc_sort_number_for_grouping_keys(keys):
    sort_number = 0

    for key in keys:
        sort_number = sort_number * GROUPING_KEYS_KEY_BASE_NUMBER + int(key) + 1

    return sort_number


def get_phrases_for_words_ordered(words_ordered, languages):
    phrases = []

    for language in languages:
        phrases_for_language = []

        for word_ordered in words_ordered:
            word = word_ordered['word']

            phrases_for_word = Phrase.objects.filter(word=word, language=language)

            phrases_for_language.append(phrases_for_word) 

        phrases.append(phrases_for_language)

    return phrases


def merge_phrases_and_images(words_ordered, phrases):
    phrases_merged = merge_phrases(words_ordered, phrases)

    phrases_and_images_merged = merge_images(words_ordered, phrases_merged)

    return phrases_and_images_merged


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

