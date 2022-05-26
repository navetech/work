from first625words.models import TransliterationSystem


def clear_data_all():
    d = TransliterationSystem.objects.all()
    d.delete()
