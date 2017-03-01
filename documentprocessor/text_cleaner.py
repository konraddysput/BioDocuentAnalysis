import string
from typing import List


class TextCleaner:
    @staticmethod
    def _remove_def_stop_words(sequence):
        default_stop_words = {'a', 'an', 'the'}
        for word in sequence:
            if word not in default_stop_words:
                yield word

    @staticmethod
    def clean_text_as_string(sequence: str) -> str:
        word_sequence = sequence.lower().translate(str.maketrans('', '', string.punctuation)).split()
        return ' '.join(TextCleaner._remove_def_stop_words(word_sequence))

    @staticmethod
    def clean_text_as_list(sequence: str) -> List[str]:
        word_sequence = sequence.lower().translate(str.maketrans('', '', string.punctuation)).split()
        return list(TextCleaner._remove_def_stop_words(word_sequence))
