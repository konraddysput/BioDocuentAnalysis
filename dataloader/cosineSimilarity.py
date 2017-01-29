from typing import List
from scipy import spatial

Vector = List[float]

from dataloader.simRegresion import SimRegresion


class CosineSimularity(SimRegresion):
    def similarity(self, vector_a: Vector, vector_b: Vector) -> float:
        return spatial.distance.cosine(vector_a, vector_b)
