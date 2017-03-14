import numpy as np
import pandas as pd
from typing import Tuple, List

from queryexpander.semantic_similarity import CppSemanticSimilarity


class QueryExpander:
    def __init__(self, vocabulary_path: str, vocabulary_length: int, centroids_file_path: str, idfs_cache_file: str):
        self._words: List[str] = pd.read_csv(
            vocabulary_path, sep=' ', quoting=3, header=None, usecols=(0,), na_filter=False).values.squeeze().tolist()
        self._vectors: np.ndarray = pd.read_csv(vocabulary_path, sep=' ', quoting=3, header=None,
                                                usecols=range(1, vocabulary_length + 1), na_filter=False,
                                                dtype=np.float32).values

        self._similarity = CppSemanticSimilarity(self._words, self._vectors, centroids_file_path, idfs_cache_file)

    def generate_sums_cache(self):
        self._similarity.generate_sums_cache()

    def generate_local_centroids(self, centroids_neighbourhood_size: int):
        self._similarity.generate_local_centroids(centroids_neighbourhood_size)

    def find_most_similar_words(self, query: List[str], number_of_results: int) -> List[Tuple[str, float]]:
        return self._similarity.find_most_similar_words(query, number_of_results)
