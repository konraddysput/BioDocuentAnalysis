import numpy as np
from scipy import spatial

from dataloader.euclidian_similarity import EuclideanSimilarity


def normalize(vector: np.ndarray):
    return vector / np.sqrt(vector.dot(vector))

class EuclideanNormalizedSimilarity(EuclideanSimilarity):
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        return spatial.distance.euclidean(normalize(vector_a), normalize(vector_b))