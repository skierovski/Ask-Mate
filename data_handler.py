import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_HEADER_QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']


def get_all_question():
    question = {}
    record = []
    result = []
    # with open('sample_data/question.csv') as file:
    # with open(DATA_FILE_PATH) as file:
    with open('C:\CC\web\\ask_mate3\sample_data\question.csv', 'r') as file:
        for row in file:
            record = row.split(",")
            if len(record) == 7:
                for index, value in enumerate(DATA_HEADER_QUESTION):
                    question[value] = record[index]
                result.append(question)
                question = {}
    return result


def get_all_answer():
    answer = {}
    record = []
    result = []
    # with open('sample_data/question.csv') as file:
    # with open(DATA_FILE_PATH) as file:
    with open('C:\CC\web\\ask_mate3\sample_data\\answer.csv', 'r') as file:
        for row in file:
            record = row.split(",")
            if len(record) == 6:
                for index, value in enumerate(DATA_HEADER_ANSWER):
                    answer[value] = record[index]
                result.append(answer)
                answer = {}
    return result


if __name__ == '__main__':
    res = get_all_question()
    print(res)
