class StopWords:
    stop_words = [None]
    def __init__(self):
        with open('../data/stopwords.txt', 'r') as stopWordsFile:
            self.stop_words= stopWordsFile.read().split(',')

    def is_stop_word(self, word):
        return word in self.stop_words

    def to_short_sentence(self, sentence):
        sentence_words = sentence.split(' ')
        return [x for x in sentence_words if x not in self.stop_words]

# if __name__ == '__main__':
#     stop_words = StopWords()
#     testCorrectStopWord= stop_words.is_stop_word("is")
#     testUncorrectStopWord = stop_words.is_stop_word("elephant")
#     short_sentence = stop_words.to_short_sentence("Tom is eating banana")
