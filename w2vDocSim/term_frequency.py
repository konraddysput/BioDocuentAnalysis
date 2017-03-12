from math import log


class TermFrequency:
    documents = []

    def __init__(self, total_documents):
        self.documents = total_documents

    def total_words_in_document(self):
        count = 0
        for item in self.documents:
            count += len(item.split())
        return count

    def count_word_in_documents(self, frequency):
        count = 0
        for string in self.documents:
            for word in string.split():
                if(word == frequency):
                    count += 1
        return count

    def calculate_term_frequency(self, word):
        return self.count_word_in_documents(word) / self.total_words_in_document()

    def calculate_inverse_document_frequency(self, word):
        return log(len(self.documents) / self.word_in_documents(word))

    def word_in_documents(self, word):
        return [word in s.split(' ') for s in self.documents].count(True)

# if __name__ == '__main__':
#     documents = [" to jest test ktory sprawdzi czy slowo jest zawarte w stringu", "jem banana", "kupie  test test krakersy",
#                  "testcik"]
#     frequence = TermFrequency(documents)
#     count = frequence.count_word_in_documents("test")
#     print(count)
#
#
#     count = frequence.word_in_documents("test")
#     print(count)
#
#     result = frequence.calculate_inverse_document_frequency("test")
#     print(result)
#
#     result = frequence.calculate_term_frequency("test")
#     print(result)
