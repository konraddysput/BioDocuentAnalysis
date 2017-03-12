from w2vDocSim.w2vDictionary import W2vDictionary
from w2vDocSim.bioNLP import BioNLP
from vocabularytester.similarity import CosineSimilarity
import xml.etree.ElementTree as ET
import gzip
import os
import re
from subprocess import call
from typing import Iterator, Iterable
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def _parse_document(document: str):
    # We have to define some entities and replace invalid occurrences of & symbol
    document = '''<!DOCTYPE doc [
    <!ENTITY rsqb ']'>
    <!ENTITY lsqb '['>
    <!ENTITY equals '='>
    <!ENTITY plus '+'>
    ]>
    ''' + re.sub(r'(\s)&(\s)', r'\g<1>&amp;\g<2>', document)

    return ElementTree.fromstring(document)


def load_from_directory(path: str) -> Iterator[Element]:
    with open(path, 'rb') as archive:
        data = str(archive.read())
        separated_documents = re.findall('(<DOC>.*?</DOC>)', data, re.DOTALL)

        for document in separated_documents:
            yield _parse_document(document)

def element_to_object(element: Element):
    obj = {}
    obj['docno'] = element.find("DOCNO").text
    obj['title'] = element.find("TITLE").text
    obj['key'] = element.find("KEYWORDS").text
    obj['desc'] = element.find("DESCRIPTION").text
    return obj

if __name__ == '__main__':
    elements = load_from_directory('biocaddieTerrier.xml')
    for element in elements:
        print(element_to_object(element))

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