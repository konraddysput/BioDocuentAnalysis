from dataloader.model import LanguageModel
from dataloader.sim_regression import SimRegression
from typing import List

class QueryExpander:
    def __init__(self, model: LanguageModel):
        self.model = model

    def p7(self, word1: str, word2: str, topn: int):
        similars = self.model.find_most_similar_words(word2, topn)
        numerator = self.model.similarity(word1, word2)
        denominator = 0
        for word3, score in similars:
            denominator += self.model.similarity(word3, word2)
        if denominator != 0:
            return numerator/denominator

    def p8(self, word: str, query: List[str], topn: int):
        prob = 0
        query_length = len(query)
        for term in query:
            term_count = 0
            for term2 in query:
                if term2 == term:
                    term_count += 1
            prob += self.p7(word, term, topn) * term_count/query_length
        return prob

    def ExpandQuery(self, query: List[str], limit = 20):
        expanded = list(query)
        tmp = dict()
        for term in query:
            tmp[term] = self.p8(term, query, limit)
        #return expanded
        return tmp