from django.shortcuts import render

# from django.http import HttpResponse

from first625words.models import Theme
from first625words.models import BaseWord
from first625words.models import Word
from first625words.models import Language


# Create your views here.

def index(request):
    themes = Theme.objects.all()

    languages = Language.objects.all()

    rows = []

    for theme in themes:
        base_words = BaseWord.objects.filter(theme=theme)

        for base_word in base_words:
            words = Word.objects.filter(base_word=base_word)

            words_ordered = order_words_by_grouping_key(words)

            phrases = get_phrases_for_words_ordered(words_ordered, languages)

            first625words = merge_phrases_and_images(phrases)

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



def order_words_by_grouping_key(words):
    pass


def get_phrases_for_words_ordered(words_ordered, languages):
    pass


def merge_phrases_and_images(phrases):
    pass
