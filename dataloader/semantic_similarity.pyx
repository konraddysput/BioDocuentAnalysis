import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.utility cimport pair
from libcpp.set cimport set


cdef inline float _cosine(np.ndarray[np.float32_t, ndim=1] vector_a, np.ndarray[np.float32_t, ndim=1] vector_b):
    cdef float denominator_a = np.sum(np.square(vector_a))
    cdef float denominator_b = np.sum(np.square(vector_b))

    return 1 - np.sum(np.dot(vector_a, vector_b)) / np.sqrt(denominator_a * denominator_b)

cpdef float calculate_similarity(np.ndarray vector_a, np.ndarray vector_b, np.ndarray vocabulary, redis):
    cdef float numerator = _cosine(vector_a, vector_b)
    cdef float denominator = 0.0

    for i in range(len(vocabulary)):
        denominator += _cosine(vocabulary[i], vector_b)

    if denominator != 0:
        print(numerator / denominator)
        return numerator / denominator


cpdef float calculate_sum_py(np.ndarray[np.float32_t, ndim=1] vector, np.ndarray[np.float32_t, ndim=2] vocabulary):
    cdef float denominator = 0.0
    for i in range(len(vocabulary)):
        denominator += _cosine(vocabulary[i], vector)

    return denominator


cdef extern from "../libraries/document-search-accelerator/accelerator.hpp":
    cdef cppclass SemanticSimilarity:
        SemanticSimilarity(vector[string] words, float *vocabulary, int rows, int cols)
        void generate_sums_cache()
        float calculate_similarity(float *vector_a, float *vector_b, int length)
        vector[pair[string, float]] find_most_similar_words(set[string] query, int number)


cdef class CppSemanticSimilarity:
    cdef SemanticSimilarity *_semantic_similarity

    def __cinit__(self, words_list, np.ndarray[np.float32_t, ndim=2] vocabulary):
        cdef vector[string] words
        words.reserve(len(words_list))
        for word in words_list:
            if not isinstance(word, str):
                print(word)
            words.push_back(word.encode())

        cdef np.ndarray[np.float32_t, ndim=2, mode="c"] vocabulary_contiguous = np.ascontiguousarray(vocabulary,
                                                                                                     dtype=np.float32)
        self._semantic_similarity = new SemanticSimilarity(words, <float *>vocabulary_contiguous.data,
                                                           vocabulary.shape[1], vocabulary.shape[0])

    def __dealloc__(self):
        del self._semantic_similarity

    cpdef void generate_sums_cache(self):
        self._semantic_similarity.generate_sums_cache()

    cpdef float calculate_similarity(self, np.ndarray[np.float32_t, ndim=1] vector_a,
                                     np.ndarray[np.float32_t, ndim=1] vector_b):
        cdef np.ndarray[np.float32_t, ndim=1, mode="c"] vector_a_contiguous = np.ascontiguousarray(vector_a,
                                                                                                   dtype=np.float32)
        cdef np.ndarray[np.float32_t, ndim=1, mode="c"] vector_b_contiguous = np.ascontiguousarray(vector_b,
                                                                                                   dtype=np.float32)

        return self._semantic_similarity.calculate_similarity(<float *>vector_a_contiguous.data,
                                                              <float *>vector_b_contiguous.data,
                                                              vector_a.shape[0])

    cpdef vector[pair[string, float]] find_most_similar_words(self, query, int number):
        cdef set[string] query_words
        for word in query:
            query_words.insert(word.encode())

        return self._semantic_similarity.find_most_similar_words(query_words, number)
