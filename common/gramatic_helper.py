class GramaticHelper:

    @staticmethod
    def clean_gramatic_as_string(sequence):
        word_sequence = sequence.split()
        word_sequence = GramaticHelper.remove_interpuction(word_sequence)
        word_sequence = GramaticHelper.remove_def_stop_words(word_sequence)
        word_sequence = GramaticHelper.to_lower(word_sequence)
        return ' '.join(word_sequence)

    @staticmethod
    def clean_gramatic_as_string(sequence):
        word_sequence = sequence.split()
        word_sequence = GramaticHelper.remove_interpuction(word_sequence)
        word_sequence = GramaticHelper.remove_def_stop_words(word_sequence)
        return GramaticHelper.to_lower(word_sequence)

    @staticmethod
    def remove_interpuction(sequence):
        interpunction_charactes = {'.', ',', ':', ';', '-', '?', '!', '(', ')', '"'}
        for word in sequence:
            for character in interpunction_charactes:
                if character in word:
                    word = word.replace(character, '')
            yield word
    @staticmethod
    def remove_def_stop_words(sequence):
        default_stop_words = {'a', 'the'}
        for word in sequence:
            if word not in default_stop_words:
                yield word

    @staticmethod
    def to_lower(sequence):
        return [item.lower() for item in sequence]

'''if __name__ == '__main__':
    print(gramatic_helper.clean_gramatic("Jhon is going to home... to take a shower? No he isn't! He want go play football, or basketball"))
'''