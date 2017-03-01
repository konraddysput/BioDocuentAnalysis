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


def load_from_directories(paths: Iterable[str]) -> Iterator[Element]:
    for directory_path in paths:
        directory = os.scandir(directory_path)
        for entry in directory:
            if entry.name.endswith('.Z'):
                # File is compressed with legacy method and must be converted to a modern format
                if call(['znew', entry.path]) != 0:
                    raise SystemError(f'Converting archive format of {file.name} failed')

                path = re.sub('\.Z$', '.gz', entry.path)
            elif entry.name.endswith('.gz'):
                # File is in a valid format
                path = entry.path
            else:
                # This aren't the documents we're looking for
                continue

            with open(path, 'rb') as archive:
                archived_file: str = gzip.decompress(archive.read()).decode('windows-1252')
                separated_documents = re.findall('(<DOC>.*?</DOC>)', archived_file, re.DOTALL)

                for document in separated_documents:
                    yield _parse_document(document)
