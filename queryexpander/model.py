import numpy as np
import pandas as pd
from typing import Tuple, List

from queryexpander.semantic_similarity import CppSemanticSimilarity
from queryexpander.sim_regression import SimRegression


class LanguageModel:
    def __init__(self, path: str, classifier: SimRegression = None):
        self._words: List[str] = pd.read_csv(
            path, sep=' ', quoting=3, header=None, usecols=(0,), na_filter=False).values.squeeze().tolist()
        self._vectors: np.ndarray = pd.read_csv(path, sep=' ', quoting=3, header=None, usecols=range(1, 51),
                                                na_filter=False, dtype=np.float32).values

        self._similarity = CppSemanticSimilarity(self._words, self._vectors)

    def generate_sums_cache(self):
        self._similarity.generate_sums_cache()

    def find_most_similar_words(self, query: List[str], number_of_results: int) -> List[Tuple[str, float]]:
        return self._similarity.find_most_similar_words(query, number_of_results)
