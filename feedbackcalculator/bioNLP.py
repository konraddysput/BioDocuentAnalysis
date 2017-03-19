import numpy as np
from sortedcontainers import SortedListWithKey
from typing import Dict, Any, List

from vocabularytester.similarity import SimRegression
from feedbackcalculator.term_frequency import calculate_term_frequencies, calculate_inverse_document_frequencies
from feedbackcalculator.w2vDictionary import W2vDictionary


class BioNLP:
    def __init__(self, similarity: SimRegression, w2v: W2vDictionary, docs: List[Dict[str, Any]], avgsl: int=0):
        self._similarity = similarity
        self._w2v = w2v
        self._docs = docs
        self._docs_idfs = calculate_inverse_document_frequencies([doc['text'] for doc in docs], self._w2v.dictionary)
        self._avgsl = avgsl

    def _calculate_vector_for_text(self, text: str, idfs: np.ndarray) -> np.ndarray:
        text_split = text.split(' ')
        tfs = calculate_term_frequencies(text_split, self._w2v.dictionary)

        scalar = 0
        vector = np.zeros(shape=(self._w2v.vocabulary_length,), dtype=np.float64)
        for word in text_split:
            try:
                word_index = self._w2v.dictionary[word]
                tf_idf = tfs[word_index] * idfs[word_index]
                vector += self._w2v.get_vector_from_index(word_index) * tf_idf
                scalar += tf_idf
            except KeyError:
                pass

        return vector / scalar

    def meth_distance(self, queries: List[str]):
        for i, doc in enumerate(self._docs):
            vector = self._calculate_vector_for_text(doc['text'], self._docs_idfs)
            doc['vector'] = vector

        queries_idfs = calculate_inverse_document_frequencies(queries, self._w2v.dictionary)

        results = []
        for i, query in enumerate(queries):
            vector = self._calculate_vector_for_text(query, queries_idfs)
            distances = SortedListWithKey(key=lambda distance: distance['distance'])

            for doc in self._docs:
                distance = self._similarity.calculate_similarity(vector, doc['vector'])
                distances.add({
                    'docno': doc['docno'],
                    'distance': distance
                })

            results.append((i, distances[:100]))

        return results

    def _semantic_similarity(self, mainWord: str, sentence: str):
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

    def semantic_text_similarity(self, text: str, query: str, k: float, b: float):
        text_split = text.split(" ")
        query_split = query.split(" ")
        text_set = set(text_split)
        sum = 0
        for word in text_set:
            sem = self._semantic_similarity(word, query)
            bracket = 1 - b + (b * len(query_split) / self._avgsl)
            word_index = self._w2v.dictionary[word]
            sum += self._docs_idfs[word_index] * (sem * (k + 1)) / (sem + k * bracket)
        return sum
