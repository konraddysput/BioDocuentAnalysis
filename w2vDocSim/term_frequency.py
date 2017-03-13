from math import log


class TermFrequency:

    def total_words_in_document(self):
        count = 0
        for item in self.documents:
            count += len(item.split())
        return count

    def count_word_in_document(self, word, sentence):
        count = 0
        for sentenceWord in sentence:
            if(word == sentenceWord):
                count += 1
        return count

    def calculate_term_frequency(self, word, document):
        splitedDocument = document.split()
        return self.count_word_in_document(word, splitedDocument) / len(splitedDocument)

    def calculate_inverse_document_frequency(self, word, documents):
        return log(len(documents) / self.word_in_documents(word,documents))

    def word_in_documents(self, word, documents):
        return [word in s.split(' ') for s in documents].count(True)

# if __name__ == '__main__':
#     documents = [" to jest test ktory sprawdzi czy slowo jest zawarte w stringu", "jem banana", "kupie  test test krakersy",
#                  "testcik"]
#     termFrequency = TermFrequency()
#     print(termFrequency.calculate_term_frequency("test", documents[0]))
#     print(termFrequency.calculate_inverse_document_frequency("test", documents))
#     print(termFrequency.word_in_documents("test", documents))

