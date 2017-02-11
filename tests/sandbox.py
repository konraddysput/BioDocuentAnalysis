from dataloader.model import LanguageModel
from dataloader.cosine_sigmoid_similarity import CosineSigmoidSimilarity
from dataloader.euclidian_similarity import EuclideanSimilarity
from query.query_expander import QueryExpander
import random

if __name__ == '__main__':
    random.seed(2017)
    cosine_sigmoid_similarity = CosineSigmoidSimilarity(5, 1)
    model = LanguageModel('glove.6B.50d.txt')
    model.classifier = cosine_sigmoid_similarity
    query_expander = QueryExpander(model)
    print(query_expander.ExpandQuery(['dog', 'hates', 'cat']))