from math import log

def count_words_in_document(document):
    count = 0
    for item in document:
        count += len(item.split())
    return count

def calculate_term_frequency(word, documents):
    return word_in_documents(word, documents) / count_words_in_document(documents)

def calculate_inverse_document_frequenct(word, documents):
    return log(len(documents)/word_in_documents(word,documents))

def word_in_documents(word, documents):
    return list(word in s for s in documents).count(1)

#if __name__ == '__main__':
#    documents = [" to jest test ktory sprawdzi czy slowo jest zawarte w stringu", "jem banana", "kupie krakersy","testcik"]
#
#    count = count_words_in_document(documents)
#    print(count)
#
#    result = calculate_inverse_document_frequenct("test", documents)
#    print(result)
#
#    result = calculate_term_frequency("test", documents)
#    print(result)


