from typing import List
Vector = List[float]
from abc import ABCMeta, abstractmethod

class SimRegresion(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def similarity(self, vector_a: Vector, vector_b: Vector) -> float:
        ...