#!/usr/bin/env python3

import click

from vocabularytester.similarity import CosineSimilarity
from vocabularytester.tester import measure_effectiveness


@click.command()
@click.argument('vocabulary_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('vocabulary_length', required=True, type=int)
@click.argument('data_path', required=True, type=click.Path(exists=True, dir_okay=False))
def run_test(vocabulary_path: str, vocabulary_length: int, data_path: str):
    print(measure_effectiveness(vocabulary_path, vocabulary_length, data_path, CosineSimilarity()))

if __name__ == '__main__':
    run_test()
