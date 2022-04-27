import os
import additional_functions
from flask import request
import database_common

DATA_FILE_PATH_QUESTION = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWER = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER_QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']


@database_common.connection_handler
def get_questions(cursor):
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor, q_id):
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            WHERE id = %s
            ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_answer(cursor, q_id):
    query = """
           SELECT id, submission_time, vote_number, question_id, message, image
           FROM answer
           WHERE question_id = %s
           ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor):
    query = """
           SELECT id, submission_time, vote_number, question_id, message, image
           FROM answer
           ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor):
    upload_file = request.files['file']
    image_name = additional_functions.file_operation(upload_file)
    message = request.form['message']
    title = request.form.get('title', default="")
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
        VALUES (now(), 0, 0, %s, %s, %s);    
    """
    cursor.execute(query, (title, message, image_name))


@database_common.connection_handler
def get_last_id(cursor):
    query = """
            SELECT max(id) FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


def create_list_to_write(list):
    list_to_return = []
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
