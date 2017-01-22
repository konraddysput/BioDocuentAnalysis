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
        try:
            document_to_insert['fileid'] = document.find('FILEID').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['note'] = document.find('NOTE').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['unk'] = document.find('UNK').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['first'] = document.find('FIRST').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['second'] = document.find('SECOND').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['head'] = document.find('HEAD').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['dateline'] = document.find('DATELINE').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['text'] = document.find('TEXT').text.strip()
        except AttributeError:
            pass
        try:
            document_to_insert['byline'] = document.find('BYLINE').text.strip()
        except AttributeError:
            pass

        self._ap_documents.insert_one(document_to_insert)

    def close(self):
        self._client.close()
