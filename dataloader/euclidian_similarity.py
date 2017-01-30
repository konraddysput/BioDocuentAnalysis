import numpy as np
from scipy import spatial

from dataloader.sim_regression import SimRegression


class EuclideanSimilarity(SimRegression):
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        return spatial.distance.euclidean(vector_a, vector_b)
