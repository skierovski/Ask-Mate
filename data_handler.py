from flask import request
import additional_functions

import database_common


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
    #new_submission = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
    new_title = request.form.get('title', default="")  # poprawic
    new_message = request.form['message']
    upload_file = request.files['file']
    new_image = additional_functions.file_operation(upload_file)
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
        VALUES (now(), 0, 0, %s, %s, %s);    
    """
    cursor.execute(query, (new_title, new_message, new_image))

@database_common.connection_handler
def get_last_id(cursor):
    query = """
            SELECT max(id) FROM question"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def add_answer(cursor,question_id):
    new_message = request.form['message']
    upload_file = request.files['file_answer']
    new_image = additional_functions.file_operation(upload_file)
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
        VALUES (now(), 0, %s, %s, %s);    
    """
    cursor.execute(query, (question_id, new_message, new_image))


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id= %s;
    """
    query_1 = """
        DELETE FROM answer
        WHERE question_id= %s;
    """
    query_2 = """
            DELETE FROM comment
            WHERE question_id= %s;
        """
    query_3 = """
                DELETE FROM question_tag
                WHERE question_id= %s;
            """
    cursor.execute(query_3, (question_id,))
    cursor.execute(query_2, (question_id,))
    cursor.execute(query_1, (question_id,))
    cursor.execute(query, (question_id,))

@database_common.connection_handler
def update_question(cursor, question_id):
    new_title = request.form.get('title', default="")
    new_message = request.form['message']
    query = """
        UPDATE question 
        SET title= %s, message =%s
     WHERE id = %s;
    """
    cursor.execute(query, (new_title,new_message,question_id))


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
           DELETE
           FROM answer
           WHERE id = %s"""
    query_1 = """
            DELETE
            FROM comment
            WHERE answer_id = %s"""

    cursor.execute(query_1, (answer_id,))
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def get_id(cursor, answer_id):
    query = """
           SELECT question_id
           FROM answer
           WHERE id = %s"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()
@database_common.connection_handler
def vote(cursor, table, direction, id):
    if table == 'question':
        query = """
            UPDATE question
            SET vote_number = vote_number + %s
            WHERE id = %s
        """
    else:
        query = """
                UPDATE answer
                SET vote_number = vote_number + %s
                WHERE id = %s
            """
    cursor.execute(query, (direction, id))