from dataloader.model import LanguageModel
from dataloader.sim_regression import SimRegression
from typing import List

class QueryExpander:
    def __init__(self, model: LanguageModel):
        self.model = model
    def ExpandQuery(self, query: List[str], topn = 1):
        expanded = list(query)
        for term in query:
            most_similars = self.model.find_most_similar_words(term, topn)
            for similar, score in most_similars:
                if similar not in expanded:
                    expanded.append(similar)
        return expanded