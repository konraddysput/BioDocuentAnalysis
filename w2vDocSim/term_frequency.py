from math import log

import numpy as np
from typing import List, Dict


class TermFrequency:
    def calculate_term_frequency(self, word, split_document):
        return split_document.count(word) / len(split_document)

    def calculate_inverse_document_frequencies(self, documents, index_map: Dict[str, int]) -> np.ndarray:
        idfs = np.zeros((len(index_map), 1), dtype=np.uint32)

        for document in documents:
            split_document = document.split()
            added_words = set()
            for word in split_document:
                if word in index_map and word not in added_words:
                    added_words.add(word)
                    idfs[index_map[word]] += 1

        return np.log(1 / idfs * len(documents))

    def word_in_documents(self, word, documents):
        return [word in s.split(' ') for s in documents].count(True)

# if __name__ == '__main__':
#     documents = [" to jest test ktory sprawdzi czy slowo jest zawarte w stringu", "jem banana", "kupie  test test krakersy",
#                  "testcik"]
#     termFrequency = TermFrequency()
#     print(termFrequency.calculate_term_frequency("test", documents[0]))
#     print(termFrequency.calculate_inverse_document_frequency("test", documents))
#     print(termFrequency.word_in_documents("test", documents))

