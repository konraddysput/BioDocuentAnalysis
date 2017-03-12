from math import log

def total_words_in_document(document):
    count = 0
    for item in document:
        count += len(item.split())
    return count

def count_word_in_documents(frequency, documents):
    count = 0
    for string in documents:
        for word in string.split():
            if(word == frequency):
                count += 1
    return count

def calculate_term_frequency(word, documents):
    return count_word_in_documents(word, documents) / total_words_in_document(documents)

def calculate_inverse_document_frequenct(word, documents):
    return log(len(documents) / word_in_documents(word, documents))

def word_in_documents(word, documents):
    return [word in s.split(' ') for s in documents].count(True)

# if __name__ == '__main__':
#     documents = [" to jest test ktory sprawdzi czy slowo jest zawarte w stringu", "jem banana", "kupie  test test krakersy",
#                  "testcik"]
#
#     count = count_word_in_documents("test", documents)
#     print(count)
#
#
#     count = word_in_documents("test", documents)
#     print(count)
#
#     result = calculate_inverse_document_frequenct("test", documents)
#     print(result)
#
#     result = calculate_term_frequency("test", documents)
#     print(result)
