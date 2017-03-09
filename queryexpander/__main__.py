#!/usr/bin/env python3

import click

from queryexpander.expansion import QueryExpander


@click.group()
def cli():
    pass


@click.command()
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
def generate_cache(vocabulary_path: str):
    query_expander = QueryExpander(vocabulary_path)
    query_expander.generate_sums_cache()


@click.command()
@click.argument('query', required=True, type=str)
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('number_of_additional_words', required=True, type=int)
def expand(query: str, vocabulary_path: str, number_of_additional_words: int):
    query_expander = QueryExpander(vocabulary_path)
    print(query_expander.find_most_similar_words(query.rstrip('\n').lower().split(' '), number_of_additional_words))


@click.command()
@click.argument('input_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('number_of_additional_words', required=True, type=int)
def expand_file(input_file_path: str, output_file_path: str, vocabulary_path: str, number_of_additional_words: int):
    query_expander = QueryExpander(vocabulary_path)

    with open(input_file_path) as input_file:
        with open(output_file_path, 'w') as output_file:
            for line in input_file:
                output_file.write(query_expander.find_most_similar_words(line.rstrip('\n').lower().split(' '),
                                                                         number_of_additional_words))

cli.add_command(generate_cache)
cli.add_command(expand)
cli.add_command(expand_file)

if __name__ == '__main__':
    cli()
