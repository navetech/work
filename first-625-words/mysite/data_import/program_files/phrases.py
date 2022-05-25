from first625words.models import Phrase


def clear_data_all():
    d = Phrase.objects.all()
    d.delete()
