from first625words.models import Phrase


def get_data_all():
    return Phrase.objects.all()


def get_data(word=None, spelling=None, language=None):
    if word:
        if spelling:
            d = Phrase.objects.filter(
                word=word, spelling=spelling
                )
        else:
            d = Phrase.objects.filter(word=word)
    elif spelling:
        d = Phrase.objects.filter(spelling=spelling)
    else:
        d = None

    return d


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(word, spelling):
    d = Phrase(word=word, spelling=spelling)

    d.save()

    return d
