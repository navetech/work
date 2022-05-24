import os


SORT_NUMBER_DEFAULT = 0
SORT_NUMBER_INC_DEFAULT = 1

DATA_FILES_DIR_NAME = 'data_files'
DATA_FILES_DIR = os.path.join('../', DATA_FILES_DIR_NAME)
DATA_FILES_EXTENSION = '.csv'
DATA_FILES_FILE_NAME_ROOTS_SEPARATOR = '_'

THEMES_FILE_NAME_ROOT = 'themes'
THEME_COLUMN = 0
THEME_HEADER = 'Theme'

BASE_WORDS_FILE_NAME_ROOT = 'base-words'
BASE_WORD_COLUMN = 0
BASE_WORD_HEADER = 'Base Word'

BASE_WORDS_LIMIT_MAX_BY_THEME = 1000

WORDS_FILE_NAME_ROOT = 'words'
WORD_BASE_WORD_COLUMN = BASE_WORD_COLUMN
WORD_BASE_WORD_HEADER = BASE_WORD_HEADER
WORD_GROUPING_COLUMN = 1
WORD_GROUPING_HEADER = 'Grouping'
WORD_GROUPING_KEY_COLUMN = 2
WORD_GROUPING_KEY_HEADER = 'Grouping Key'

IMAGES_FILE_NAME_ROOT = 'images'
IMAGE_BASE_WORD_COLUMN = WORD_BASE_WORD_COLUMN
IMAGE_BASE_WORD_HEADER = WORD_BASE_WORD_HEADER
IMAGE_GROUPING_COLUMN = WORD_GROUPING_COLUMN
IMAGE_GROUPING_HEADER = WORD_GROUPING_HEADER
IMAGE_GROUPING_KEY_COLUMN = WORD_GROUPING_KEY_COLUMN
IMAGE_GROUPING_KEY_HEADER = WORD_GROUPING_KEY_HEADER
IMAGE_COLUMN = 3
IMAGE_HEADER = 'Image'

LANGUAGES_FILE_NAME_ROOT = 'languages'
LANGUAGE_COLUMN = 0
LANGUAGE_HEADER = 'Language'

"""
WORDS_SPELLINGS_FILE_NAME_ROOT = 'words-spellings'
SPELLING_BASE_WORD_COLUMN = BASE_WORD_COLUMN
SPELLING_BASE_WORD_HEADER = BASE_WORD_HEADER
SPELLING_GROUPING_COLUMN = GROUPING_COLUMN
SPELLING_GROUPING_HEADER = GROUPING_HEADER
SPELLING_GROUPING_KEY_COLUMN = GROUPING_KEY_COLUMN
SPELLING_GROUPING_KEY_HEADER = GROUPING_KEY_HEADER
SPELLING_COLUMN = 3
SPELLING_HEADER = 'Spelling'
SPELLING_ALT_COLUMN = 4
SPELLING_ALT_HEADER = 'Alt Spelling'

SPELLINGS_FILE_NAME_ROOT = 'spellings'
PRONUNCIATIONS_FILE_NAME_ROOT = 'pronunciations'
PRONUNCIATION_SPELLING_COLUMN = 0
PRONUNCIATION_SPELLING_HEADER = SPELLING_HEADER
PRONUNCIATION_SOUND_COLUMN = 1
PRONUNCIATION_SOUND_HEADER = 'Pronunciation Sound'
PRONUNCIATION_PRONUNC_SPELL_COLUMN = 2
PRONUNCIATION_PRONUNC_SPELL_HEADER = 'Pronunciation Spelling'
PRONUNCIATION_PRONUNC_SPELL_LANG_COLUMN = 3
PRONUNCIATION_PRONUNC_SPELL_LANG_HEADER = 'Pronunciation Spelling Language'
"""