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

    languages = []
#    language = Language.objects.filter(name='Chinese').first()
#    languages.append(language)
    language = Language.objects.filter(name='English').first()
    languages.append(language)
    language = Language.objects.filter(name='Portuguese').first()
    languages.append(language)

    themes = []
    theme = Theme.objects.filter(name='Animal').first()
    themes.append(theme)

    data = build_words_page(languages, themes)

    context = {
        'data': data
    }

    return render(request, 'first625words/words.html', context)

    # return HttpResponse("Hello, world. You're at the first625words index.")


def build_words_page(languages, themes):
    data = {}

    themes_data_list = []
    for theme in themes:
        theme_data = build_words_page_from_theme(theme, languages)
        themes_data_list.append(theme_data)

    counting = calc_list_counting(themes_data_list)

    data['languages'] = languages
    data['counting'] = counting
    data['for_themes'] = themes_data_list

    return data


def calc_list_counting(data_list):
    counting = {}

    images_and_languages_counting = (
        calc_list_images_and_languages_counting(data_list)
    )

    counting['images'] = images_and_languages_counting['images']
    counting['languages'] = images_and_languages_counting['languages']

    languages_countings = []
    languages_count = len(images_and_languages_counting['languages'])
    for language_index in range(languages_count):

        one_language_counting = calc_list_one_language_counting(
            data_list, language_index
            )

        languages_countings.append(one_language_counting)

    counting['for_languages'] = languages_countings

    return counting


def calc_list_images_and_languages_counting(data_list):
    counting = {}
    counting['images'] = []
    counting['languages'] = []

    images_count_max = 0
    languages_count_max = 0

    for data in data_list:
        data_counting = data['counting']

        images_count = len(data_counting['images'])
        if images_count > images_count_max:
            images_count_max = images_count

            counting['images'] = data_counting['images']

        languages_count = len(data_counting['languages'])
        if languages_count > languages_count_max:
            languages_count_max = languages_count

            counting['languages'] = data_counting['languages']

    return counting


def calc_list_one_language_counting(data_list, language_index):
    counting = {}

    phrases_counting = calc_list_phrases_counting(data_list, language_index)

    counting['phrases'] = phrases_counting

    phrases_countings = []
    phrases_count = len(phrases_counting)
    for phrase_index in range(phrases_count):

        one_phrase_counting = calc_list_one_phrase_counting(
            data_list, language_index, phrase_index
            )
        phrases_countings.append(one_phrase_counting)

    counting['for_phrases'] = phrases_countings

    return counting


def calc_list_phrases_counting(data_list, language_index):
    counting = []

    phrases_count_max = 0

    for data in data_list:
        data_counting = data['counting']

        languages_count = len(data_counting['for_languages'])

        if language_index < languages_count:
            one_language_counting = data_counting['for_languages'][language_index]
            phrases = one_language_counting['phrases']

            phrases_count = len(phrases)
            if phrases_count > phrases_count_max:
                phrases_count_max = phrases_count

                counting = phrases

    return counting


def calc_list_one_phrase_counting(data_list, language_index, phrase_index):
    counting = {}

    pronunciations_counting = calc_list_pronunciations_counting(
        data_list, language_index, phrase_index
        )

    counting['pronunciations'] = pronunciations_counting

    return counting


def calc_list_pronunciations_counting(data_list, language_index, phrase_index):
    counting = []

    pronunciations_count_max = 0

    for data in data_list:
        data_counting = data['counting']

        languages_count = len(data_counting['for_languages'])

        if language_index < languages_count:
            one_language_counting = data_counting['for_languages'][language_index]
            phrases = one_language_counting['phrases']

            phrases_count = len(phrases)
            if phrase_index < phrases_count:

                one_phrase_counting = (
                    one_language_counting['for_phrases'][phrase_index]
                )

                pronunciations = one_phrase_counting['pronunciations']

                pronunciations_count = len(pronunciations)
                if pronunciations_count > pronunciations_count_max:
                    pronunciations_count_max = pronunciations_count

                    counting = pronunciations

    return counting


def build_words_page_from_theme(theme, languages):
    data = {}

    base_words = BaseWord.objects.filter(theme=theme).all().order_by('sort_number')

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

    words = Word.objects.filter(base_word=base_word).all()

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

    ordered_words.sort(key=lambda e: e['key_number'])

    return ordered_words


def calc_key_number_for_grouping_key(grouping_key):
    keys = grouping_key.split(GROUPING_KEYS_KEYS_SEPARATOR)

    key_number = 0
    for key in keys:
        if str(key):
            key_number = key_number * GROUPING_KEYS_KEY_BASE_NUMBER + int(key) + 1

    return key_number


def build_rows_from_words(ordered_words, languages):
    languages_ordered_phrases = get_languages_ordered_phrases(
        ordered_words, languages
        )

    phrases_mergings = merge_phrases(
        ordered_words, languages_ordered_phrases
        )

    mergings = merge_images(ordered_words, phrases_mergings)

    rows = []
    for merging in mergings:
        row = build_row_from_merging(merging)

        if row:
            rows.append(row)

    return rows


def get_languages_ordered_phrases(ordered_words, languages):
    languages_ordered_phrases = []

    for language in languages:
        one_language_ordered_phrases = []

        for ordered_word_index in range(len(ordered_words)):
            ordered_word = ordered_words[ordered_word_index]
            word = ordered_word['word']

            phrases = Phrase.objects.filter(word=word, language=language).all()

            if phrases.count() > 0:
                phrases_data = {}
                phrases_data['phrases'] = phrases
                phrases_data['index'] = ordered_word_index
                phrases_data['merged'] = False

                one_language_ordered_phrases.append(phrases_data)
        
        languages_ordered_phrases.append(
            one_language_ordered_phrases
            )

    return languages_ordered_phrases


def merge_phrases(ordered_words, languages_ordered_phrases):
    mergings = []

    last_grouping_ordered_word_index = 0
    last_grouping = None
    
    languages_ordered_phrases_indexes = [0] * len(languages_ordered_phrases)

    while True:

        data = build_phrases_merging(
            ordered_words,
            languages_ordered_phrases, languages_ordered_phrases_indexes,
            last_grouping, last_grouping_ordered_word_index
            )

        if not data:
            break

        mergings.append(data['merging'])

        grouping_equivalences = data['grouping_equivalences']
        if True in grouping_equivalences:
            last_grouping = data['grouping']
        else:
            last_grouping = None

        languages_ordered_phrases_indexes = data['indexes']

        last_grouping_ordered_word_index = data['last_index']

    return mergings


def build_phrases_merging(
        ordered_words,
        languages_ordered_phrases, languages_ordered_phrases_indexes,
        last_grouping, last_grouping_ordered_word_index
        ):

    if last_grouping_ordered_word_index >= len(ordered_words):
        return None

    if last_grouping is not None:
        grouping = last_grouping
    else:
        languages_ordered_phrases_indexes = get_languages_ordered_phrases_indexes(
            languages_ordered_phrases, last_grouping_ordered_word_index
            )

        ordered_word_index = get_ordered_word_index(
            languages_ordered_phrases, languages_ordered_phrases_indexes
            )

        if ordered_word_index is None or ordered_word_index >= len(ordered_words):
            return None

        ordered_word = ordered_words[ordered_word_index]
        word = ordered_word['word']
        grouping = word.grouping

        last_grouping_ordered_word_index = ordered_word_index + 1

    languages_mergings = []

    languages_count = len(languages_ordered_phrases)
    languages_grouping_equivalences = [False] * languages_count

    for language_index in range(languages_count):
        one_language_phrases_index = languages_ordered_phrases_indexes[language_index]

        one_language_ordered_phrases = languages_ordered_phrases[language_index]
        
        one_language_merging = {}
        one_language_merging['phrases'] = []
        one_language_merging['word'] = None

        while (
            one_language_phrases_index
            <
            len(one_language_ordered_phrases)
        ):

            phrases_data = one_language_ordered_phrases[one_language_phrases_index]
            one_language_phrases_index += 1

            if phrases_data['merged']:
                continue

            ordered_words_phrases_index = phrases_data['index']

            one_language_ordered_word = (
                ordered_words[ordered_words_phrases_index]
            )

            one_language_word = one_language_ordered_word['word']

            one_language_grouping = one_language_word.grouping

            groupings_cmp_direct = compare_groupings(
                grouping, one_language_grouping, reverse=False
            )

            groupings_cmp_reverse = compare_groupings(
                grouping, one_language_grouping, reverse=True
            )

            if (
                last_grouping is None
                or
                (str(last_grouping) and not str(last_grouping).isspace())
            ):

                # groupings_equivalent_direct = groupings_cmp_direct == 0 or groupings_cmp_direct == -1
                groupings_equivalent_direct = groupings_cmp_direct <= 0
                groupings_equivalent_reverse = groupings_cmp_reverse <= 0
            else:
                groupings_equivalent_direct = groupings_cmp_direct == 0
                groupings_equivalent_reverse = groupings_cmp_reverse == 0

            """
            groupings_cmp_reverse = compare_groupings(
                grouping, one_language_grouping, reverse=True
            )

            groupings_equivalent_direct = groupings_cmp_direct <= 0
            groupings_equivalent_reverse = groupings_cmp_reverse <= 0
            """

            if groupings_equivalent_direct or groupings_equivalent_reverse:
#            if groupings_equivalent_direct:
                one_language_merging['phrases'] = phrases_data['phrases']
                one_language_merging['word'] = one_language_word
                phrases_data['merged'] = True

                languages_ordered_phrases_indexes[language_index] = one_language_phrases_index

                languages_grouping_equivalences[language_index] = True

                break

        languages_mergings.append(one_language_merging)

    merging = {
        'for_languages': languages_mergings        
    }

    data = {
        'merging': merging,
        'indexes': languages_ordered_phrases_indexes,
        'grouping': grouping, 
        'grouping_equivalences': languages_grouping_equivalences,
        'last_index': last_grouping_ordered_word_index
    }

    return data


def get_languages_ordered_phrases_indexes(
        languages_ordered_phrases, last_grouping_ordered_word_index
        ):

    languages_count = len(languages_ordered_phrases)
    languages_ordered_phrases_indexes = [0] * languages_count

    for language_index in range(languages_count):
        one_language_ordered_phrases = languages_ordered_phrases[language_index]

        languages_ordered_phrases_indexes[language_index] = len(one_language_ordered_phrases)
        for one_language_phrases_index in range(len(one_language_ordered_phrases)):

            phrases_data = one_language_ordered_phrases[one_language_phrases_index]
            ordered_words_phrases_index = phrases_data['index']

            if ordered_words_phrases_index >= last_grouping_ordered_word_index:
                languages_ordered_phrases_indexes[language_index] = one_language_phrases_index

                break

    return languages_ordered_phrases_indexes


def get_ordered_word_index(
        languages_ordered_phrases, languages_ordered_phrases_indexes
        ):

        ordered_words_indexes = []

        languages_count = len(languages_ordered_phrases)
        for language_index in range(languages_count):
            one_language_ordered_phrases = languages_ordered_phrases[language_index]
            phrases_index = languages_ordered_phrases_indexes[language_index]

            if phrases_index < len(one_language_ordered_phrases):
                phrases_data = one_language_ordered_phrases[phrases_index]

                ordered_words_indexes.append(phrases_data['index'])

        if len(ordered_words_indexes) > 0:
            ordered_word_index = min(ordered_words_indexes)
        else:
            ordered_word_index = None

        return ordered_word_index


def compare_groupings(grouping1, grouping2, reverse=False):
    if grouping1 == grouping2:
        return 0
    elif is_grouping1_in_grouping2(grouping1, grouping2, reverse):
        return -1
    elif is_grouping1_in_grouping2(grouping2, grouping1, reverse):
        return -2
    else:
        return 1


def is_grouping1_in_grouping2(grouping1, grouping2, reverse=False):
    if not str(grouping1) or str(grouping1).isspace():
        return True

    if grouping1 == grouping2:
        return True

    groups1 = grouping1.split(GROUPING_GROUPS_SEPARATOR)
    groups2 = grouping2.split(GROUPING_GROUPS_SEPARATOR)

    if reverse:
        groups1.reverse()
        groups2.reverse()

    for group_index in range(len(groups1)):
        if groups1[group_index] != groups2[group_index]:
            return False

    return True


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
                if not one_language_word:
                    continue

                one_language_grouping = one_language_word.grouping

                groupings_cmp_direct = compare_groupings(
                    grouping, one_language_grouping, reverse=False
                )

                groupings_equivalent_direct = groupings_cmp_direct <= 0

                if groupings_equivalent_direct and not images_merged:
                    for image in images:
                        if image not in merging['images']:
                            merging['images'].append(image)

                    images_merged = True

                    break

            if images_merged:
                break

    return mergings


def build_row_from_merging(merging):
    row = {}

    languages_phrases = []
    for one_language_merging in merging['for_languages']:

        one_language_word = one_language_merging['word']
#        if not one_language_word:
#            continue

        one_language_phrases = one_language_merging['phrases']

        languages_phrases.append(one_language_phrases)

    if len(languages_phrases) > 0:
        row['languages_phrases'] = languages_phrases

        if 'images' in merging:
            row['images'] = merging['images']
        else:
            row['images'] = []

    return row


def calc_rows_counting(rows):
    counting = {}

    images_and_languages_counting = calc_rows_images_and_languages_counting(rows)

    counting['images'] = images_and_languages_counting['images']
    counting['languages'] = images_and_languages_counting['languages']

    languages_countings = []
    languages_count = len(images_and_languages_counting['languages'])
    for language_index in range(languages_count):

        one_language_counting = calc_rows_one_language_counting(
            rows, language_index
            )

        languages_countings.append(one_language_counting)

    counting['for_languages'] = languages_countings

    return counting


def calc_rows_images_and_languages_counting(rows):
    counting = {}
    counting['images'] = []
    counting['languages'] = []

    images_count_max = 0
    languages_count_max = 0

    for row in rows:
        images_count = len(row['images'])
        if images_count > images_count_max:
            images_count_max = images_count

            counting['images'] = row['images']

        languages_count = len(row['languages_phrases'])
        if languages_count > languages_count_max:
            languages_count_max = languages_count

            counting['languages'] = list(range(languages_count_max))

    return counting


def calc_rows_one_language_counting(rows, language_index):
    counting = {}

    phrases_counting = calc_rows_phrases_counting(rows, language_index)

    counting['phrases'] = phrases_counting

    phrases_countings = []
    phrases_count = len(phrases_counting)
    for phrase_index in range(phrases_count):

        one_phrase_counting = calc_rows_one_phrase_counting(
            rows, language_index, phrase_index
            )
        phrases_countings.append(one_phrase_counting)

    counting['for_phrases'] = phrases_countings

    return counting


def calc_rows_phrases_counting(rows, language_index):
    counting = []

    phrases_count_max = 0

    for row in rows:
        languages_count = len(row['languages_phrases'])

        if language_index < languages_count:
            phrases = row['languages_phrases'][language_index]

            phrases_count = len(phrases)
            if phrases_count > phrases_count_max:
                phrases_count_max = phrases_count

                counting = phrases

    return counting


def calc_rows_one_phrase_counting(rows, language_index, phrase_index):
    counting = {}

    pronunciations_counting = calc_rows_pronunciations_counting(
        rows, language_index, phrase_index
        )

    counting['pronunciations'] = pronunciations_counting

    return counting


def calc_rows_pronunciations_counting(rows, language_index, phrase_index):
    counting = []

    pronunciations_count_max = 0

    for row in rows:
        languages_count = len(row['languages_phrases'])

        if language_index < languages_count:
            phrases = row['languages_phrases'][language_index]
            phrases_count = len(phrases)

            if phrase_index < phrases_count:
                phrase = phrases[phrase_index]

                pronunciations = phrase.pronunciations.all()

                pronunciations_count = len(pronunciations)
                if pronunciations_count > pronunciations_count_max:
                    pronunciations_count_max = pronunciations_count

                    counting = pronunciations

    return counting
