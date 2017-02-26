import pandas as pd
from collections import Counter
import re

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
        print(f'useless words: {uselessWords}')

        for query in self.queriesWords:
            print(query)
