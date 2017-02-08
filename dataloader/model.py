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
        self._words: List[str] = pd.read_csv(
            path, sep=' ', quoting=3, header=None, usecols=(0,), na_filter=False).values.squeeze().tolist()
        self._vectors: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=range(1, 51),
                                                na_filter=False, dtype=np.float32).values

        self._similarity = CppSemanticSimilarity(self._words, self._vectors)

    def generate_sums_cache(self):
        self._similarity.generate_sums_cache()

    def find_most_similar_words(self, word: str, number_of_results: int) -> List[Tuple[str, float]]:
        return self._similarity.find_most_similar_words(word, number_of_results)
