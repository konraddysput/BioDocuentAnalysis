from dataloader.model import LanguageModel
from dataloader.cosineSimilarity import CosineSimularity
from dataloader.euclidianSimilarity import EuclidianSimilarity
import random

if __name__ == "__main__":
    random.seed(2017)
    model = LanguageModel("glove.6B.50d.txt")
    words: list = ["the", "duck", "ran", "away", "from", "angry", "hunter", "using", "wings",
                   "plane", "crashed", "into", "building",
                   "motorcycle", "hit", "other", "car",
                   "hell", "yes",
                   "birds", "bird", "birdie", "pigeon", "heron", "seagull",
                   "tree", "forest", "grass", "oxygen", "animal", "squirrel", "deer",
                   "dear", "ms", "mr",
                   "queen", "king", "kingdom", "majesty", "heritage", "wealth"]
    cossim = CosineSimularity()
    euclsim = EuclidianSimilarity()
    for i in range(0, 500):
        word1: str = random.choice(words)
        word2: str = random.choice(words)
        print("Words: %s, %s" % (word1, word2))
        model.classifier = cossim
        print("Cosine sim: %f" % model.similarity(word1, word2))
        model.classifier = euclsim
        print("Euclidian sim: %f" % model.similarity(word1, word2))
        print()