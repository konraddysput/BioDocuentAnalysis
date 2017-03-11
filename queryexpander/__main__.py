#!/usr/bin/env python3

import click

from queryexpander.expansion import QueryExpander


@click.group()
def cli():
    pass


@click.command()
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_length', required=True, type=int)
@click.argument('sums_cache_file', required=True, type=str)
def generate_cache(vocabulary_path: str, vocabulary_length: int, sums_cache_file: str):
    query_expander = QueryExpander(vocabulary_path, vocabulary_length, sums_cache_file)
    query_expander.generate_sums_cache()


@click.command()
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_length', required=True, type=int)
@click.argument('sums_cache_file', required=True, type=str)
@click.argument('centroids_neighbourhood_size', required=True, type=int)
@click.argument('centroids_file_path', required=True, type=str)
def generate_centroids(vocabulary_path: str, vocabulary_length: int, sums_cache_file: str,
                       centroids_neighbourhood_size: int, centroids_file_path: str):
    query_expander = QueryExpander(vocabulary_path, vocabulary_length, sums_cache_file, centroids_file_path)
    query_expander.generate_local_centroids(centroids_neighbourhood_size)


@click.command()
@click.argument('query', required=True, type=str)
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_length', required=True, type=int)
@click.argument('number_of_additional_words', required=True, type=int)
@click.argument('sums_cache_file', required=True, type=str)
def expand(query: str, vocabulary_path: str, vocabulary_length: int, number_of_additional_words: int,
           sums_cache_file: str):
    query_expander = QueryExpander(vocabulary_path, vocabulary_length, sums_cache_file)
    print(query_expander.find_most_similar_words(query.rstrip('\n').lower().split(' '), number_of_additional_words))


@click.command()
@click.argument('input_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_length', required=True, type=int)
@click.argument('number_of_additional_words', required=True, type=int)
@click.argument('sums_cache_file', required=True, type=str)
def expand_file(input_file_path: str, output_file_path: str, vocabulary_path: str, vocabulary_length: int,
                number_of_additional_words: int, sums_cache_file: str):
    query_expander = QueryExpander(vocabulary_path, vocabulary_length, sums_cache_file)

    with open(input_file_path) as input_file:
        with open(output_file_path, 'w') as output_file:
            for line in input_file:
                output_file.write(query_expander.find_most_similar_words(line.rstrip('\n').lower().split(' '),
                                                                         number_of_additional_words))

cli.add_command(generate_cache)
cli.add_command(generate_centroids)
cli.add_command(expand)
cli.add_command(expand_file)

if __name__ == '__main__':
    cli()
