import numpy as np
from sortedcontainers import SortedListWithKey
from typing import Dict, Any, List

from vocabularytester.similarity import SimRegression
from feedbackcalculator.term_frequency import calculate_term_frequencies, calculate_inverse_document_frequencies
from feedbackcalculator.w2vDictionary import W2vDictionary


class BioNLP:
    def __init__(self, similarity: SimRegression, w2v: W2vDictionary):
        self._similarity = similarity
        self._w2v = w2v

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

    def meth_distance(self, docs: List[Dict[str, Any]], queries: List[str]):
        docs_texts = [doc['text'] for doc in docs]
        docs_idfs = calculate_inverse_document_frequencies(docs_texts, self._w2v.dictionary)

        for i, doc in enumerate(docs):
            vector = self._calculate_vector_for_text(doc['text'], docs_idfs)
            doc['vector'] = vector

        queries_idfs = calculate_inverse_document_frequencies(queries, self._w2v.dictionary)

        results = []
        for i, query in enumerate(queries):
            vector = self._calculate_vector_for_text(query, queries_idfs)
            distances = SortedListWithKey(key=lambda distance: distance['distance'])

            for doc in docs:
                distance = self._similarity.calculate_similarity(vector, doc['vector'])
                distances.add({
                    'docno': doc['docno'],
                    'distance': distance
                })

            results.append((i, distances[:100]))

        return results

    def semantic_similarity(self, mainWord: str, sentence: str):
        # FIXME: probably broken by refactor
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
        # FIXME: broken by refactor
        text_split = text.split(" ")
        query_split = query.split(" ")
        text_set = set(text_split)
        sum = 0
        for word in text_set:
            idf = self._tf.calculate_inverse_document_frequency(word, docs)
            sem = self.semantic_similarity(word, query)
            bracket = 1 - b + (b * len(query_split) / avgsl)
            sum += idf * (sem * (k + 1)) / (sem + k * bracket)
        return sum
