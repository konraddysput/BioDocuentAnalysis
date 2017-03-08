import random

from queryexpander.expansion import LanguageModel

if __name__ == '__main__':
    random.seed(2017)
    model = LanguageModel('glove.6B.50d.txt')

    with open('QUERIES') as file:
        for line in file:
            print(model.find_most_similar_words(line.rstrip('\n').lower().split(' '), 10))

    # print(model.find_most_similar_words(["beaver", "lives", "water"], 10))
    # model.generate_sums_cache()
    # print(model.find_most_similar_words(["dog"], 10))
