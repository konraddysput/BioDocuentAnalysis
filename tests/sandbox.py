from dataloader.model import LanguageModel
from dataloader.cosine_similarity import CosineSimilarity
import random

def semantic_sim(model: LanguageModel, word1: str, word2: str):
    numerator = model.similarity(word1, word2)
    denominator = 0
    for word3, index in model._dictionary.items():
        denominator += model.similarity(word3, word2)
    if denominator != 0:
        return numerator/denominator
    return None

if __name__ == '__main__':
    random.seed(2017)
    cosine_similarity = CosineSimilarity()
    model = LanguageModel('glove.6B.50d.txt', cosine_similarity)
    print(semantic_sim(model, "dog", "majesty"))