import numpy as np
from typing import List, Dict


def calculate_term_frequencies(split_document: List[str], index_map: Dict[str, int]) -> np.ndarray:
    occurrences = np.zeros((len(index_map),), dtype=np.uint32)
    for word in split_document:
        if word in index_map:
            occurrences[index_map[word]] += 1

    return occurrences / len(split_document)


def calculate_inverse_document_frequencies(documents: List[str], index_map: Dict[str, int]) -> np.ndarray:
    if len(documents) == 1:
        # TODO: is this a valid action for one-document collection?
        return np.ones((len(index_map),), dtype=np.uint32)

    occurrences = np.zeros((len(index_map),), dtype=np.uint32)

    for document in documents:
        split_document = document.split()
        added_words = set()
        for word in split_document:
            if word in index_map and word not in added_words:
                added_words.add(word)
                occurrences[index_map[word]] += 1

    with np.errstate(divide='ignore'):
        idfs = np.log(len(documents) / occurrences)
        idfs[idfs == np.inf] = 0.0
        return idfs
