from typing import List
Vector = List[float]

from dataloader.simRegresion import SimRegresion

class CosineSimularity(SimRegresion):

    def similarity(self, vector_a: Vector, vector_b: Vector) -> float:
        return vector_a[0] * vector_b[0]