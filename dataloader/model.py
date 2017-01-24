from operator import itemgetter
from random import randint
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd


class LanguageModel:
    def __init__(self, path: str):
        words: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=(0,)).values.squeeze()

        self._dictionary: Dict[str, int] = dict(zip(words, range(len(words))))
        self._vectors: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=range(1, 51)).values

    @staticmethod
    def _get_score(*_):
        # Mock
        return randint(0, 1000000)

    def find_most_similar_words(self, word: str, number_of_results: int) -> List[Tuple[str, float]]:
        vector_for_word: np.ndarray = self._vectors[self._dictionary[word]]
        scores: Dict[str, int] = {}
        for word, index in self._dictionary.items():
            scores[word] = self._get_score(vector_for_word, self._vectors[index])

        return sorted(scores.items(), key=itemgetter(1))[:number_of_results]
