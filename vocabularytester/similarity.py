from abc import ABCMeta, abstractmethod

import pandas as pd
from typing import List, Dict

import numpy as np
from scipy import spatial


class SimRegression(metaclass=ABCMeta):
    @abstractmethod
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        ...


class EuclideanSimilarity(SimRegression):
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        return spatial.distance.euclidean(vector_a, vector_b)


class NormalizedEuclideanSimilarity(EuclideanSimilarity):
    @staticmethod
    def _normalize(vector: np.ndarray):
        return vector / np.sqrt(vector.dot(vector))

    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        return spatial.distance.euclidean(self._normalize(vector_a), self._normalize(vector_b))


class CosineSimilarity(SimRegression):
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        return spatial.distance.cosine(vector_a, vector_b)


class CosineSigmoidSimilarity(SimRegression):
    def __init__(self, a: float, c: float):
        self._a = a
        self._c = c

    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + 2.71828182846 ** (-self._a * (x - self._c)))

    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        return self._sigmoid(spatial.distance.cosine(vector_a, vector_b))


class SimilarityCalculator:
    def __init__(self, vocabulary_path: str, similarity_function: SimRegression):
        words: List[str] = pd.read_csv(vocabulary_path, sep=' ', quoting=3, header=None, usecols=(0,),
                                       na_filter=False).values.squeeze()

        self._dictionary: Dict[str, int] = dict(zip(words, range(len(words))))
        self._vectors: np.ndarray = pd.read_csv(vocabulary_path, sep=' ', quoting=3, header=None, usecols=range(1, 51),
                                                na_filter=False, dtype=np.float32).values

        self._similarity = similarity_function

    def calculate_similarity(self, first_word: str, second_word: str) -> float:
        return self._similarity.calculate_similarity(self._vectors[self._dictionary[first_word]],
                                                     self._vectors[self._dictionary[second_word]])
