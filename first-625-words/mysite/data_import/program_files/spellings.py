from first625words.models import Spelling


def clear_data_all():
    d = Spelling.objects.all()
    d.delete()
