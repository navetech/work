from first625words.models import PronunciationSpelling


def get_data_all():
    return PronunciationSpelling.objects.all()


def get_data(text, system):
    d = PronunciationSpelling.objects.filter(text=text, system=system)

    return d


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(text, system):
    d = PronunciationSpelling(text=text, system=system)

    d.save()

    return d
