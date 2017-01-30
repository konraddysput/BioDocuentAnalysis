from dataloader.model import LanguageModel
from dataloader.cosine_similarity import CosineSimilarity
from dataloader.euclidian_similarity import EuclideanSimilarity
import random

if __name__ == '__main__':
    random.seed(2017)
    cosine_similarity = CosineSimilarity()
    euclidean_similarity = EuclideanSimilarity()
    model = LanguageModel('glove.6B.50d.txt', cosine_similarity)
    words: list = ['the', 'duck', 'ran', 'away', 'from', 'angry', 'hunter', 'using', 'wings',
                   'plane', 'crashed', 'into', 'building',
                   'motorcycle', 'hit', 'other', 'car',
                   'hell', 'yes',
                   'birds', 'bird', 'birdie', 'pigeon', 'heron', 'seagull',
                   'tree', 'forest', 'grass', 'oxygen', 'animal', 'squirrel', 'deer',
                   'dear', 'ms', 'mr',
                   'queen', 'king', 'kingdom', 'majesty', 'heritage', 'wealth']

    for i in range(0, 500):
        word1: str = random.choice(words)
        word2: str = random.choice(words)
        print(f'Words: {word1}, {word2}')
        model.classifier = cosine_similarity
        print(f'Cosine sim: {model.similarity(word1, word2)}')
        model.classifier = euclidean_similarity
        print(f'Euclidian sim: {model.similarity(word1, word2)}')
        print()

    for i in range(0, 500):
        word1: str = random.choice(words)
        print(f'Our today word is {word1}')
        most_similar_words = model.find_most_similar_words(word1, 1000)
        for word, similarity in most_similar_words:
            print(f'Word: {word}, Similarity: {similarity}')
