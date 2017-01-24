#!/usr/bin/env python3

from typing import Tuple

import click

from dataloader.database import DatabaseManager
from dataloader.loading import load_from_directories


@click.group()
def cli():
    pass


@click.command()
@click.argument('directories', nargs=-1, required=True, type=click.Path(exists=True, file_okay=False))
def load_tipster(directories: Tuple[str]):
    with DatabaseManager() as database:
        loader = load_from_directories(directories)
        count: int = 0

        for document in loader:
            database.add_ap_document(document)

            count += 1
            print(f'\r{count} documents inserted', end='')

        print('\nLoading finished')

cli.add_command(load_tipster)

if __name__ == '__main__':
    cli()
