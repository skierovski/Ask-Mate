import os

DATA_FILE_PATH_QUESTION = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWER = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER_QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']


def get_all_question(question_id=None):
    question = {}
    result = []
    select_question = []
    with open(DATA_FILE_PATH_QUESTION, "r") as file:
        for row in file:
            record = row.split(",")
            if len(record) == 7:
                for index, value in enumerate(DATA_HEADER_QUESTION):
                    question[value] = record[index].rstrip("\n")
                result.append(question)
                question = {}
    if question_id != None:
        for item in result:
            if item['id'] == question_id:
                select_question = item
        return select_question
    return result


def get_all_answer(answer_id=None):
    answer = {}
    result = []
    select_answer = []
    with open(DATA_FILE_PATH_ANSWER, 'r') as file:
        for row in file:
            record = row.split(",")
            if len(record) == 6:
                for index, value in enumerate(DATA_HEADER_ANSWER):
                    answer[value] = record[index].rstrip("\n")
                result.append(answer)
                answer = {}
    if answer_id != None:
        for item in result:
            if item['question_id'] == answer_id:
                select_answer.append(item)
        return select_answer
    return result


def create_list_to_write(list):
    list_to_return=[]
    for item in list:
        list_to_return.append(item.values())
    return list_to_return


def write_table_to_file_question(table, separator=','):
    with open(DATA_FILE_PATH_QUESTION, "w") as file:
        for record in table:
            row = separator.join(record)
            file.write(row + "\n")


def write_table_to_file_answer(table, separator=','):
    with open(DATA_FILE_PATH_ANSWER, "w") as file:
        for record in table:
            row = separator.join(record)
            file.write(row + "\n")


if __name__ == '__main__':
    res = get_all_question()
    print(res)
