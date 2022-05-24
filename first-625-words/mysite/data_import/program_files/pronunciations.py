from first625words.models import Pronunciation


def get_data_all():
    return Pronunciation.objects.all()


def get_data(sound, spelling):
    if spelling is not None:
        d = Pronunciation.objects.filter(
            sound=sound, spelling=spelling
            )
    else:
        d = Pronunciation.objects.filter(
            sound=sound, spelling__isnull=True
            )

    return d


def clear_data_all():
    d = get_data_all()
    d.delete()


def insert_data(sound, spelling):
    d = Pronunciation(sound=sound, spelling=spelling)

    d.save()

    return d
