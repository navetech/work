from first625words.models import PronunciationSpelling


def clear_data_all():
    d = PronunciationSpelling.objects.all()
    d.delete()
