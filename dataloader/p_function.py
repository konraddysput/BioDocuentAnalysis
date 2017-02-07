import numpy as np
from dataloader.sim_regression import SimRegression
from dataloader.model import LanguageModel
from typing import Dict

class PFunction(SimRegression):
    def __init__(self, language_model: LanguageModel, classifier: SimRegression):
        self.classifier: SimRegression = classifier
        self.language_model: LanguageModel = language_model

    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        numerator = self.classifier.calculate_similarity(vector_a, vector_b)
        denominator = 0
        for word3, index in self.language_model._dictionary.items():
            vector_c: np.ndarray = self.language_model._vectors[index]
            if not np.array_equal(vector_c, vector_b):
                classifier_sim = self.classifier.calculate_similarity(vector_c, vector_b)
                denominator += classifier_sim
        if denominator != 0:
            sim = numerator / denominator
            return sim