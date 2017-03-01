import string
from typing import List


def clean_text_as_list(sequence: str) -> List[str]:
    default_stop_words = {'a', 'an', 'the'}
    word_sequence = sequence.lower().translate(str.maketrans('', '', string.punctuation)).split()
    return [word for word in word_sequence if word not in default_stop_words]


def clean_text_as_string(sequence: str) -> str:
    default_stop_words = {'a', 'an', 'the'}
    word_sequence = sequence.lower().translate(str.maketrans('', '', string.punctuation)).split()
    return ' '.join([word for word in word_sequence if word not in default_stop_words])
