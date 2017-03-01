import re

class GramaticHelper:

    @staticmethod
    def clean_gramatic_file(file_path):
        with open(file_path, encoding="utf8") as file:
            for word_sequence_line in file:
                word_sequence_line = word_sequence_line.strip()
                if not word_sequence_line:
                    continue
                word_sequence_line = GramaticHelper.remove_interpuction(word_sequence_line)
                word_sequence_line = GramaticHelper.to_lower(word_sequence_line)
                yield GramaticHelper.remove_def_stop_words(word_sequence_line)


    @staticmethod
    def clean_gramatic_as_list(sequence):
        word_sequence = sequence.split()
        word_sequence = GramaticHelper.remove_interpuction(word_sequence)
        word_sequence = GramaticHelper.remove_def_stop_words(word_sequence)
        return GramaticHelper.to_lower(word_sequence)

    @staticmethod
    def remove_interpuction(sequence):
        interpunction_charactes = {'.', ',', ':', ';', '-', '?', '!', '(', ')', '"'}
        return re.sub('[.,:;-?!()"]', '', sequence)

    @staticmethod
    def remove_def_stop_words(sequence):
        default_stop_words = {'a', 'the'}

        querywords = sequence.split()
        resultwords = [word for word in querywords if word not in default_stop_words]
        return ' '.join(resultwords)

    @staticmethod
    def to_lower(sequence):
        return sequence.lower()

'''if __name__ == '__main__':
   # print(gramatic_helper.clean_gramatic("Jhon is going to home... to take a shower? No he isn't! He want go play football, or basketball"))
   result = GramaticHelper.clean_gramatic_file('../data/test.txt')
   for sequence in result:
        print(''.join(sequence))'''