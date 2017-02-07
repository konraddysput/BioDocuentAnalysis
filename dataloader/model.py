from operator import itemgetter
from typing import Dict, Tuple, List

import redis

from dataloader.semantic_similarity import calculate_similarity, CppSemanticSimilarity
import numpy as np
import pandas as pd
import time

from dataloader.sim_regression import SimRegression


class LanguageModel:
    def __init__(self, path: str, classifier: SimRegression = None):
        words: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=(0,)).values.squeeze()

        self._dictionary: Dict[str, int] = dict(zip(words, range(len(words))))
        self._vectors: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=range(1, 51),
                                                dtype=np.float32).values

        self.classifier: SimRegression = classifier
        self._similarity = CppSemanticSimilarity(self._vectors)

    def similarity(self, word1: str, word2: str):
        if word1 in self._dictionary and word2 in self._dictionary:
            return self._similarity.calculate_similarity(self._vectors[self._dictionary[word1]],
                                                         self._vectors[self._dictionary[word2]])
        return None

    def find_most_similar_words(self, word: str, number_of_results: int) -> List[Tuple[str, float]]:
        print(self._similarity.find_most_similar_words(self._dictionary[word], number_of_results))

        return None
