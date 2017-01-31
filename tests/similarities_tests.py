import pandas as pd
from dataloader.sim_regression import SimRegression
from dataloader.model import LanguageModel
from dataloader.cosine_similarity import CosineSimilarity
from dataloader.euclidian_similarity import EuclideanSimilarity


def get_answer(model: LanguageModel, question: str, words):
    probably_answer = ''
    max_sim = 10
    for w in words[0]:
        sim = model.similarity(question, w)
        if sim < max_sim:
            probably_answer = w
            max_sim = sim
    return probably_answer


def processing_data(path, sim_regression: SimRegression):
    df = pd.read_csv(path, sep='\t')
    correct_answer = 0
    model = LanguageModel('glove.6B.50d.txt', sim_regression)
    questions_count = df.shape[0]
    for i, row in enumerate(df.values):
        question = row[0]
        words = [row[1:row.size - 1]]
        answer = row[row.size - 1]

        probably_answer = get_answer(model, question, words)

        print('Question: ' + str(question))
        # print('Words: ' + ''.join(words, ','))
        print('Your answer: ' + probably_answer + ', correct answer: ' + answer)
        if answer == probably_answer:
            correct_answer += 1
            print('Correct!')
        else:
            print('Wrong!')
        print('--------------')

    print('Correct answers: ' + str(correct_answer) +
          ', all questions: ' + str(questions_count) +
          ', effectiveness: ' + str(correct_answer / questions_count))


processing_data('esl.txt', CosineSimilarity())
