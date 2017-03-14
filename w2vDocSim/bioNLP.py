import numpy as np

from vocabularytester.similarity import SimRegression
from w2vDocSim.w2vDictionary import W2vDictionary
from w2vDocSim.term_frequency import TermFrequency


class Object:
    pass


class BioNLP:
    def __init__(self, similarity: SimRegression, w2v: W2vDictionary):
        self._similarity = similarity
        self._w2v = w2v
        self._tf = TermFrequency()

    def meth_distance(self, docs, queries):
        results = []
        print('meth_distance')

        docs_texts = [o.text for o in docs]

        print('Calcularing doc vectors:')
        size = len(docs)
        i = 1
        for doc in docs:
            print(f'{i}/{size}')
            vector = self.calculate_vector_for_text(docs_texts, doc.text)
            doc.vector = vector
            i += 1
        print('DONE')

        i = 1
        for query in queries:
            print('query: ' + i)
            vector = self.calculate_vector_for_text(queries, query)
            distances = []
            for doc in docs:
                distance = self._similarity.calculate_similarity(vector, doc.vector)
                obj = Object()
                obj.docno = doc.docno
                obj.distance = distance
                distances.append(obj)

            distances = sorted(distances, key=lambda student: distance[1])
            obj = Object()
            obj.query = i
            obj.closest = distances[:100]
            results.append(obj)
            i += 1

        return results

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

    def calculate_vector_for_text(self, docs, text: str) -> np.ndarray:
        text_split = text.split(' ')
        scalar = 0
        vector = np.zeros(shape=(self._w2v.vocabulary_length, 1), dtype=np.float64)
        idfs = self._tf.calculate_inverse_document_frequencies(word, docs)
        for index, word in enumerate(text_split):
            tf = self._tf.calculate_term_frequency(word, text_split)
            idf = idfs[index]
            vector += self._w2v.get_word_vector(word) * tf * idf
            scalar += idf * tf

        return vector / scalar
