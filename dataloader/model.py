from operator import itemgetter
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd

from dataloader.sim_regression import SimRegression


class LanguageModel:
    def __init__(self, path: str, classifier: SimRegression = None):
        words: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=(0,)).values.squeeze()

        self._dictionary: Dict[str, int] = dict(zip(words, range(len(words))))
        self._vectors: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=range(1, 51)).values

        self.classifier: SimRegression = classifier

    def similarity(self, word1: str, word2: str):
        if word1 in self._dictionary and word2 in self._dictionary:
            return self.classifier.calculate_similarity(self._vectors[self._dictionary[word1]],
                                                        self._vectors[self._dictionary[word2]])
        return None

    def find_most_similar_words(self, word: str, number_of_results: int) -> List[Tuple[str, float]]:
        scores: Dict[str, int] = {}
        for word2, index in self._dictionary.items():
            if word2 != word:
                scores[word2] = self.similarity(word, word2)

        return sorted(scores.items(), key=itemgetter(1))[:number_of_results]
