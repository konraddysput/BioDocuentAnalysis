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
    model = LanguageModel('glove.6B.50d.txt')

    with open('QUERIES') as file:
        for line in file:
            print(model.find_most_similar_words(line.rstrip('\n').lower().split(' '), 10))

    # print(model.find_most_similar_words(["beaver", "lives", "water"], 10))
    # model.generate_sums_cache()
    # print(model.find_most_similar_words(["dog"], 10))
