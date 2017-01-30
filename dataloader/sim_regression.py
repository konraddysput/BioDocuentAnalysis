from abc import ABCMeta, abstractmethod

import numpy as np


class SimRegression(metaclass=ABCMeta):
    @abstractmethod
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        ...
