import re

from lxml import etree

import click

from vocabularytester.similarity import CosineSimilarity
from feedbackcalculator.bioNLP import BioNLP
from feedbackcalculator.w2vDictionary import W2vDictionary


@click.group()
def cli():
    pass


def get_docs(file_path: str):
    with open(file_path, 'rb') as data:
        xml = data.read()
        root = etree.fromstring(xml)

    return [document_to_dict(child) for child in root]


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


def get_queries(file_path: str):
    with open(file_path) as queries_file:
        return [re.sub('[\n.,()_]', '', line).lower() for line in queries_file]


@click.command()
@click.argument('docs_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_length', required=True, type=int)
@click.argument('query', required=True, type=str)
def get_ranking_for_query(docs_file_path: str, vocabulary_file_path: str, vocabulary_length: int, query: str):
    docs = get_docs(docs_file_path)
    model = W2vDictionary(vocabulary_file_path, vocabulary_length)
    similarity = CosineSimilarity()

    nlp = BioNLP(similarity, model, docs)
    _, documents_ranking = nlp.meth_distance([query])[0]
    for document_info in documents_ranking:
        print(f'{document_info["docno"]}/{document_info["distance"]}')


@click.command()
@click.argument('docs_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_length', required=True, type=int)
@click.argument('queries_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
def get_ranking_for_all_queries(docs_file_path: str, vocabulary_file_path: str, vocabulary_length: int,
                                queries_file_path: str):
    queries = get_queries(queries_file_path)
    docs = get_docs(docs_file_path)
    model = W2vDictionary(vocabulary_file_path, vocabulary_length)
    similarity = CosineSimilarity()
    nlp = BioNLP(similarity, model, docs)

    results = nlp.meth_distance(queries)

    for result in results:
        print(f'{result[0]}/{result[1]}')

cli.add_command(get_ranking_for_query)
cli.add_command(get_ranking_for_all_queries)

if __name__ == '__main__':
    cli()
