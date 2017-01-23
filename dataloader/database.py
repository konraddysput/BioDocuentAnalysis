from functools import partial
from operator import is_not
from xml.etree.ElementTree import Element

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class DatabaseManager:
    def __init__(self):
        self._client: MongoClient = MongoClient()
        self._db: Database = self._client.tipster
        self._ap_documents: Collection = self._db.AP

    def __enter__(self) -> 'DatabaseManager':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def add_ap_document(self, document: Element):
        document_to_insert = {
            '_id': document.find('DOCNO').text.strip()
        }

        fileid = document.find('FILEID')
        if fileid:
            document_to_insert['fileid'] = fileid.text.strip()

        unk = document.find('UNK')
        if unk:
            document_to_insert['unk'] = unk.text.strip()

        first = document.find('FIRST')
        if first:
            document_to_insert['first'] = first.text.strip()

        second = document.find('SECOND')
        if second:
            document_to_insert['second'] = second.text.strip()

        notes = document.findall('NOTE')
        if notes:
            document_to_insert['notes'] = list(
                filter(partial(is_not, None), map(lambda note: note.text.strip() if note.text else None, notes))
            )

        heads = document.findall('HEAD')
        if heads:
            document_to_insert['heads'] = list(
                filter(partial(is_not, None), map(lambda head: head.text.strip() if head.text else None, heads))
            )

        datelines = document.findall('DATELINE')
        if datelines:
            document_to_insert['datelines'] = list(map(lambda dateline: dateline.text.strip(), datelines))

        bylines = document.findall('BYLINE')
        if bylines:
            document_to_insert['bylines'] = list(map(lambda byline: byline.text.strip(), bylines))

        texts = document.findall('TEXT')
        if texts:
            document_to_insert['texts'] = list(
                filter(partial(is_not, None), map(lambda text: text.text.strip() if text.text else None, texts))
            )

        self._ap_documents.insert_one(document_to_insert)

    def close(self):
        self._client.close()
