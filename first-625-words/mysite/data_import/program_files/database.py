from . import themes
from . import base_words
from . import images
from . import words
from . import spellings
from . import languages
from . import translit_systems
from . import pronunc_spellings
from . import pronunciations
from . import phrases


def clear_data_all():
    themes.clear_data_all()
    base_words.clear_data_all()
    images.clear_data_all()
    words.clear_data_all()
    spellings.clear_data_all()
    languages.clear_data_all()
    translit_systems.clear_data_all()
    pronunc_spellings.clear_data_all()
    pronunciations.clear_data_all()
    phrases.clear_data_all()


def import_data(path=None):
    print()

    # clear_data_all()

    themes.import_data(path)
    base_words.import_data(path)
    images.import_data_for_words(path)
    languages.import_data(path)
    phrases.import_data_for_words(path)
    pronunciations.import_data_for_phrases(path)
