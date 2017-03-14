from w2vDocSim.w2vDictionary import W2vDictionary
from w2vDocSim.bioNLP import BioNLP
from vocabularytester.similarity import CosineSimilarity
from lxml import etree
import re
import time


class Object:
    pass

def get_docs2():
    with open('biocaddieTerrierValid.xml', 'rb') as data:
        xml = data.read()
        parser = etree.XMLParser(recover=True) # recover from bad characters.
        root = etree.fromstring(xml, parser=parser)

    docs = []
    for child in root:
        docs.append(element_to_object(child))
    return docs


def element_to_object(element):
    obj = Object()
    obj.docno = element.find("DOCNO").text
    title = element.find("TITLE").text
    desc = element.find("DESCRIPTION").text

    if not isinstance(title, str):
        title = ''
    if not isinstance(desc, str):
        desc = ''

    doc_text = title + ' ' + desc
    doc_text = re.sub('[\n.,()_]', '', doc_text).lower()
    obj.text = doc_text
    return obj


def get_queries():
    queries = []
    with open('../data/queries.txt') as queries_file:
        for line in queries_file:
            queries.append(re.sub('[\n.,()_]', '', line).lower())
    return queries

if __name__ == '__main__':
    queries = get_queries()
    docs = get_docs2()
    model = W2vDictionary("glove.6B.50d.txt", 50)
    similarity = CosineSimilarity()
    bioNLP = BioNLP(similarity, model)

    results = bioNLP.meth_distance(docs, queries)

    for result in results:
        print(result.query)
        print(result.closest)

    # array = ["dog rhino", "computer printer"]
    #
    # textVec1 = bioNLP.text_vector(array[0])
    # textVec2 = bioNLP.text_vector(array[1])
    #
    # catVec = model.get_word_vector("cat")
    # monitorVec = model.get_word_vector("monitor")
    #
    # dis1 = similarity.calculate_similarity(textVec1, catVec)
    # dis2 = similarity.calculate_similarity(textVec1, monitorVec)
    # dis3 = similarity.calculate_similarity(textVec2, catVec)
    # dis4 = similarity.calculate_similarity(textVec2, monitorVec)
    #
    # sem5 = bioNLP.semantic_text_similarity(array, 2, array[0], "cat", 1.2, 0.75)
    # sem6 = bioNLP.semantic_text_similarity(array, 2, array[0], "monitor", 1.2, 0.75)
    # sem7 = bioNLP.semantic_text_similarity(array, 2, array[1], "cat", 1.2, 0.75)
    # sem8 = bioNLP.semantic_text_similarity(array, 2, array[1], "monitor", 1.2, 0.75)
