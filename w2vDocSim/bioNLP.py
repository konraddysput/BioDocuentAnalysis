from typing import Dict, Any, List

import numpy as np

from vocabularytester.similarity import SimRegression
from w2vDocSim.w2vDictionary import W2vDictionary
from w2vDocSim.term_frequency import TermFrequency
from sortedcontainers import SortedListWithKey


class BioNLP:
    def __init__(self, similarity: SimRegression, w2v: W2vDictionary):
        self._similarity = similarity
        self._w2v = w2v
        self._tf = TermFrequency()

    def _calculate_vector_for_text(self, text: str, idfs: np.ndarray) -> np.ndarray:
        text_split = text.split(' ')
        scalar = 0
        vector = np.zeros(shape=(self._w2v.vocabulary_length, 1), dtype=np.float64)

        for word in text_split:
            tf = self._tf.calculate_term_frequency(word, text_split)
            idf = idfs[self._w2v.dictionary[word]]
            vector += self._w2v.get_word_vector(word) * tf * idf
            scalar += idf * tf

        return vector / scalar

    def meth_distance(self, docs: List[Dict[str, Any]], queries: List[str]):
        print('Calculating documents\' IDFs')
        docs_texts = [doc['text'] for doc in docs]
        docs_idfs = self._tf.calculate_inverse_document_frequencies(docs_texts, self._w2v.dictionary)

        print('Calculating documents\' vectors:')
        size = len(docs)
        for i, doc in enumerate(docs):
            print(f'\r{i}/{size}')
            vector = self._calculate_vector_for_text(doc['text'], docs_idfs)
            doc['vector'] = vector
        print()

        print('Calculating queries IDFs')
        queries_idfs = self._tf.calculate_inverse_document_frequencies(queries, self._w2v.dictionary)

        print('Calculating results')
        results = []
        size = len(queries)
        for i, query in enumerate(queries):
            print(f'\r{i}/{size}')
            vector = self._calculate_vector_for_text(query, queries_idfs)
            distances = SortedListWithKey(key=lambda distance: distance['distance'])

            for doc in docs:
                distances.add({
                    'docno': doc['docno'],
                    'distance': self._similarity.calculate_similarity(vector, doc['vector'])
                })

            results.append((i, distances[:100]))
        print()

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
