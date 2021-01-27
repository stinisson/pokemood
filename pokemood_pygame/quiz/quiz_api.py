import random
import requests
import base64

""" 
Quiz questions from Open Trivia DB - a free to use, user-contibuted trivia question database. https://opentdb.com/
"""

quiz_categories = {
    "Computers": 'https://opentdb.com/api.php?amount=50&category=18&type=multiple&encode=base64',
    "Mathematics": 'https://opentdb.com/api.php?amount=30&category=19&type=multiple&encode=base64',
    "Science and Nature": 'https://opentdb.com/api.php?amount=50&category=17&type=multiple&encode=base64',
    "Video Games": "https://opentdb.com/api.php?amount=50&category=15&type=multiple&encode=base64"}


def get_questions(url):
    r = requests.get(url)
    ls = r.json()['results']
    return ls


def decode_base64(string):
    return base64.b64decode(string).decode('utf-8')


def decode_base64_list(list):
    decoded = []
    for elem in list:
        decoded.append(decode_base64(elem))
    return decoded


def random_order(correct_answer, wrong_answers):
    answer_options = [correct_answer]
    for wrong_answer in wrong_answers:
        answer_options.append(wrong_answer)
    random.shuffle(answer_options)
    return answer_options


def get_quiz(number_of_questions_to_retrieve, category):
    url = quiz_categories[category]
    questions_base64 = get_questions(url)

    questions = []
    correct_answers = []
    options = []
    for idx, question_base64 in enumerate(questions_base64):

        question = decode_base64(questions_base64[idx]['question'])
        correct_answer = decode_base64(questions_base64[idx]['correct_answer'])
        incorrect_answers = decode_base64_list(questions_base64[idx]['incorrect_answers'])
        answer_options = random_order(correct_answer, incorrect_answers)

        # TODO handle if no questions have answer options with proper length
        # TODO handle requests.exceptions.ConnectionError Max retries exceeded with url
        # TODO handle Code 1: No Results Could not return results. The API doesn't have enough questions for your query.
        answer_option_too_many_chars = False
        for answer_option in answer_options:
            if len(answer_option) > 56:
                answer_option_too_many_chars = True
                break

        if answer_option_too_many_chars:
            continue

        questions.append(question)
        correct_answers.append(correct_answer)
        options.append(answer_options)

        if len(questions) == number_of_questions_to_retrieve:
            return category, questions, correct_answers, options

    print("Couldn't find any question with answer options within specified length.")
