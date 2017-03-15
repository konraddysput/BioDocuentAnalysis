import re

from lxml import etree

from vocabularytester.similarity import CosineSimilarity
from w2vDocSim.bioNLP import BioNLP
from w2vDocSim.w2vDictionary import W2vDictionary


def get_docs():
    with open('biocaddieTerrierValid.xml', 'rb') as data:
        xml = data.read()
        parser = etree.XMLParser(recover=True) # recover from bad characters.
        root = etree.fromstring(xml, parser=parser)

    return [docs.append(document_to_dict(child)) for child in root]


def document_to_dict(element):
    document = {
        'docno': element.find('DOCNO').text
    }
    title = element.find('TITLE').text
    desc = element.find('DESCRIPTION').text

    if not isinstance(title, str):
        title = ''
    if not isinstance(desc, str):
        desc = ''

    document.update({
        'title': title,
        'desc': desc,
        'text': re.sub('[\n.,()_]', '', f'{title} {desc}').lower()
    })

    return document


def get_queries():
    with open('../data/queries.txt') as queries_file:
        return [re.sub('[\n.,()_]', '', line).lower() for line in queries_file]

if __name__ == '__main__':
    queries = get_queries()
    docs = get_docs()
    model = W2vDictionary('glove.6B.50d.txt', 50)
    similarity = CosineSimilarity()
    bioNLP = BioNLP(similarity, model)

    results = bioNLP.meth_distance(docs, queries)

    for result in results:
        print(result[0])
        print(result[1])

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
