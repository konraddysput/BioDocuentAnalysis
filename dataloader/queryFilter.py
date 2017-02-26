import pandas as pd
from collections import Counter
import re
import xml.etree.ElementTree as ET

class QueryFilter:
    def __init__(self, path: str):
        with open(path) as file:
            self.queries = file.readlines()
        for i, query in enumerate(self.queries):
            self.queries[i] = re.sub('[,.()\n]', '', query)

        self.queriesWords = []
        for query in self.queries:
            self.queriesWords.append(set(query.split(" ")))

    def similarity_filter(self, threshold: float):
        dict = {}
        queryWordsDist = []
        wordCount = Counter()
        for queryWords in self.queriesWords:
            distWords = set(queryWords)
            queryWordsDist.append(distWords)
            wordCount.update(distWords)

        queriesNumber = len(self.queriesWords)
        uselessWords = set([x for x in wordCount if wordCount[x] > threshold*queriesNumber])

        self.queriesWords = [x - uselessWords for x in self.queriesWords]

    def mesh_filter(self, path: str):
        tree = ET.parse(path)
        elements = tree.findall('.//meshterm/name')
        values = set([x.text.lower() for x in elements])

        for i, query in enumerate(self.queriesWords):
            self.queriesWords[i] = set([x.lower() for x in query])

        self.queriesWords = [x & values for x in self.queriesWords]

