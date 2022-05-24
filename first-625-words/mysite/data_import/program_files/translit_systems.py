from first625words.models import TransliterationSystem


def get_data_all():
    return TransliterationSystem.objects.all()


def get_data(name):
    d = TransliterationSystem.objects.filter(name=name)

    return d


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(name):
    d = TransliterationSystem(name=name)

    d.save()

    return d
