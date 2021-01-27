import random
import requests
import base64

"""
Quiz questions from Open Trivia DB - a free to use, user-contibuted trivia question database. https://opentdb.com/
"""

quiz_categories = {
    "datateknik": 'https://opentdb.com/api.php?amount=4&category=18&difficulty=easy&type=multiple&encode=base64',
    "matematik": 'https://opentdb.com/api.php?amount=4&category=19&difficulty=medium&type=multiple&encode=base64',
    "vetenskap och natur": 'https://opentdb.com/api.php?amount=4&category=17&difficulty=medium&type=multiple&encode=base64'}


def get_all_questions(url):
    r = requests.get(url)
    ls = r.json()['results']
    return ls


def decode_base64(string):
    return base64.b64decode(string).decode('utf-8')


def decode_base64_list(list):
    decoded = []
    for elem in list:
        decoded.append(base64.b64decode(elem).decode('utf-8'))
    return decoded


def quiz_category():
    category, url = random.choice(list(quiz_categories.items()))
    return category, url


def random_order(correct_answer, wrong_answers):
    answer_options = [correct_answer]
    for wrong_answer in wrong_answers:
        answer_options.append(wrong_answer)
    random.shuffle(answer_options)
    return answer_options


def quiz():
    category, url = quiz_category()
    questions = get_all_questions(url)

    print(f"\nHär kommer fyra stycken kluriga quizfrågor inom {category}. (Try not. Do or do not. There is no try.) Lycka till!")

    incorrect_questions = []
    for idx, question_base64 in enumerate(questions):

        question = decode_base64(questions[idx]['question'])
        print(f"\nFråga {idx + 1}. {question}")

        correct_answer = decode_base64(questions[idx]['correct_answer'])
        incorrect_answers = decode_base64_list(questions[idx]['incorrect_answers'])
        answer_options = random_order(correct_answer, incorrect_answers)

        for idx, answer_option in enumerate(answer_options):
            print(f"{idx + 1}) {answer_option}")

        while True:
            try:
                answer = int(input(f"Ditt svar: "))
                if answer in range(1, len(answer_options) + 1):
                    break
            except ValueError:
                pass
            print(f"Ogiltligt svar. Ange en siffra 1-{len(answer_options)}.")

        if answer_options[answer - 1] == correct_answer:
            print("Rätt!")
        else:
            print(f"Det var fel! Rätt svar är: {answer_options.index(correct_answer) + 1}) {correct_answer}. ")
            incorrect_questions.append(question)

    print("\n-*-*- RESULTAT -*-*-")
    print(f"Du fick {4-len(incorrect_questions)} rätt av 4.")
    if len(incorrect_questions) > 0:
        print("\nDu hade fel på dessa frågor:")
        for incorrect_question in incorrect_questions:
            print(f"  - {incorrect_question}")
        return False
    return True
