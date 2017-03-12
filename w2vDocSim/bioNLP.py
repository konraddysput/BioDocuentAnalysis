from vocabularytester.similarity import SimRegression
from w2vDocSim.w2vDictionary import W2vDictionary
import numpy as np

class BioNLP:
    def __init__(self, similarity: SimRegression, w2v: W2vDictionary):
        self._similarity = similarity
        self._w2v = w2v

    def semantic_similarity(self, mainWord: str, sentence: str):
        sentenceSet = set(sentence.split(" "))
        maxSim = 0

        mainWordVector = self._w2v.get_word_vector(mainWord)
        for word in sentenceSet:
            wordVector = self._w2v.get_word_vector(word)
            distance = self._similarity.calculate_similarity(mainWordVector, wordVector)
            if distance < 0:
                distance = -distance
            similarity = 1 - distance
            if similarity > maxSim:
                maxSim = similarity
        return maxSim

    def semantic_text_similarity(self, docs, avgsl, text: str, query: str, k: float, b: float):
        textSplit = text.split(" ")
        querySplit = query.split(" ")
        textSet = set(textSplit)
        sum = 0
        for word in textSet:
            IDF = 1
            sem = self.semantic_similarity(word, query)
            bracket = 1 - b + (b * len(querySplit) / avgsl)
            sum += IDF * (sem * (k + 1)) / (sem + k * bracket)
        return sum

    def text_vector(self, text: str):
        textSplit = text.split(" ")
        scalar = 0
        vector = 0
        for word in textSplit:
            TF = 1
            IDF = 1
            vector += self._w2v.get_word_vector(word) * TF * IDF
            scalar += IDF * TF
        return vector / scalar