import numpy as np
from scipy import spatial

from queryexpander.sim_regression import SimRegression


class CosineSigmoidSimilarity(SimRegression):
    def __init__(self, a: float, c: float):
        self.a = a
        self.c = c
    def sigmoid(self, x: float):
        return 1/(1 + 2.71828182846**(-self.a*(x - self.c)))
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        return self.sigmoid(spatial.distance.cosine(vector_a, vector_b))
