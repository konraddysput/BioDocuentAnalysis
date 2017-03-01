from typing import Iterable, Optional

import re
import xml.etree.ElementTree as ET
from collections import Counter


class QueryFilter:
    def __init__(self, path: str):
        with open(path) as file:
            self._queries = file.readlines()

        for i, query in enumerate(self._queries):
            self._queries[i] = re.sub('[,.()\n]', '', query).lower()

        self._queries_words = []
        for query in self._queries:
            self._queries_words.append(set(query.split(' ')))

    def similarity_filter(self, threshold: float, queries_words: Optional[Iterable[str]]=None):
        if not queries_words:
            queries_words = self._queries_words

        query_words_dist = []
        word_count = Counter()
        for query_words in queries_words:
            dist_words = set(query_words)
            query_words_dist.append(dist_words)
            word_count.update(dist_words)

        queries_number = len(queries_words)
        useless_words = {x for x in word_count if word_count[x] > threshold * queries_number}

        return [x - useless_words for x in queries_words]

    def mesh_filter(self, path: str, queries_words: Optional[Iterable[str]]=None):
        if not queries_words:
            queries_words = self._queries_words

        tree = ET.parse(path)
        elements = tree.findall('.//meshterm/name')
        values = {x.text.lower() for x in elements}

        return [x & values for x in queries_words]
