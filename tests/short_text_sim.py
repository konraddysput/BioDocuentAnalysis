from w2vDocSim.w2vDictionary import W2vDictionary
from w2vDocSim.bioNLP import BioNLP
from vocabularytester.similarity import CosineSimilarity

if __name__ == '__main__':
    model = W2vDictionary("glove.6B.50d.txt", 50)
    similarity = CosineSimilarity()
    bioNLP = BioNLP(similarity, model)

    array = ["dog rhino", "computer printer"]

    textVec1 = bioNLP.text_vector(array[0])
    textVec2 = bioNLP.text_vector(array[1])

    catVec = model.get_word_vector("cat")
    monitorVec = model.get_word_vector("monitor")

    dis1 = similarity.calculate_similarity(textVec1, catVec)
    dis2 = similarity.calculate_similarity(textVec1, monitorVec)
    dis3 = similarity.calculate_similarity(textVec2, catVec)
    dis4 = similarity.calculate_similarity(textVec2, monitorVec)

    sem5 = bioNLP.semantic_text_similarity(array, 2, array[0], "cat", 1.2, 0.75)
    sem6 = bioNLP.semantic_text_similarity(array, 2, array[0], "monitor", 1.2, 0.75)
    sem7 = bioNLP.semantic_text_similarity(array, 2, array[1], "cat", 1.2, 0.75)
    sem8 = bioNLP.semantic_text_similarity(array, 2, array[1], "monitor", 1.2, 0.75)