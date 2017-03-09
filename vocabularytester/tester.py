import logging
import numpy as np
import pandas as pd

from vocabularytester.similarity import SimilarityCalculator, SimRegression


def __get_answer(calculator: SimilarityCalculator, question: str, words: np.ndarray):
    answer = None
    min_distance = float('inf')
    for word in words:
        distance = calculator.calculate_similarity(question, word)
        if distance < min_distance:
            answer = word
            min_distance = distance

    return answer


def measure_effectiveness(vocabulary_path: str, vocabulary_length: int, data_path: str,
                          sim_regression: SimRegression) -> float:
    data = pd.read_csv(data_path, sep=' ')
    correct_answers_count = 0
    calculator = SimilarityCalculator(vocabulary_path, vocabulary_length, sim_regression)

    for row in data.values:
        question = row[0]
        words = row[1:row.size - 1]
        correct_answer = row[row.size - 1]

        try:
            if __get_answer(calculator, question, words) == correct_answer:
                correct_answers_count += 1
        except KeyError as e:
            logging.warning(f'{e.args[0]} not in dictionary')

    return correct_answers_count / data.shape[0]
