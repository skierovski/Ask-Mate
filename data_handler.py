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
    # query_1 = """
    #     DELETE FROM answer
    #     WHERE question_id= %s;
    # """
    # query_2 = """
    #         DELETE FROM comment
    #         WHERE question_id= %s;
    #     """
    # query_3 = """
    #             DELETE FROM question_tag
    #             WHERE question_id= %s;
    #         """
    # cursor.execute(query_3, (question_id,))
    # cursor.execute(query_2, (question_id,))
    # cursor.execute(query_1, (question_id,))
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
    # query_1 = """
    #         DELETE
    #         FROM comment
    #         WHERE answer_id = %s"""

    # cursor.execute(query_1, (answer_id,))
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


@database_common.connection_handler
def get_question_comments(cursor, q_id):
    query = """
           SELECT id, answer_id, submission_time, question_id, message, edited_count
           FROM comment
           WHERE question_id = %s AND answer_id is NULL 
           ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()

@database_common.connection_handler
def add_question_comment(cursor, question_id):
    new_message = request.form['message']
    query = """
        INSERT INTO comment (question_id, message, submission_time, edited_count ) 
        VALUES (%s, %s, now(), 0);    
    """
    cursor.execute(query, (question_id, new_message))

@database_common.connection_handler
def get_answer_comments(cursor, question_id):
    query = """
           SELECT id, submission_time, question_id, answer_id, message, edited_count
           FROM comment
           WHERE question_id = %s
           ORDER BY submission_time"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()

@database_common.connection_handler
def add_answer_comment(cursor, answer_id, question_id):
    new_message = request.form['message']
    query = """
        INSERT INTO comment (question_id,answer_id, message, submission_time, edited_count ) 
        VALUES (%s, %s, %s, now(), 0);    
    """
    cursor.execute(query, (question_id[0]['question_id'],answer_id, new_message))

@database_common.connection_handler
def search_question(cursor, search_phrase):
    query = """
            SELECT * FROM question
            WHERE title like '%{}%' or message like '%{}%'   
        """.format(search_phrase,search_phrase)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_answer(cursor, search_phrase):
    query = """
            SELECT * FROM answer
            WHERE message like '%{}%'   
        """.format(search_phrase)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_answer(cursor, answer_id):
    new_message = request.form['message']
    query = """
        UPDATE answer 
        SET message =%s
     WHERE id = %s;
    """
    cursor.execute(query, (new_message, answer_id))

@database_common.connection_handler
def get_answer_to_edit(cursor, q_id):
    query = """
           SELECT id, submission_time, vote_number, question_id, message, image
           FROM answer
           WHERE id = %s
           ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_to_edit(cursor, c_id):
    query = """
           SELECT *
           FROM comment
           WHERE id = %s
           ORDER BY submission_time"""
    cursor.execute(query, (c_id,))
    return cursor.fetchall()

@database_common.connection_handler
def update_comment(cursor, comment_id):
    new_message = request.form['message']
    query = """
        UPDATE comment 
        SET edited_count = edited_count + 1, message =%s, submission_time = now()
     WHERE id = %s;
    """
    cursor.execute(query, (new_message, comment_id))


@database_common.connection_handler
def get_q_id_from_comment(cursor, comment_id):
    query = """
           SELECT question_id
           FROM comment
           WHERE id = %s"""
    cursor.execute(query, (comment_id,))
    return cursor.fetchall()

@database_common.connection_handler
def delete_comment(cursor, comment_id):
    query = """
            DELETE
            FROM comment
            WHERE id = %s"""
    cursor.execute(query, (comment_id,))


@database_common.connection_handler
def get_n_last_question(cursor, n):
    query = """
           SELECT * 
           FROM question 
           ORDER BY submission_time desc limit %s;"""
    cursor.execute(query, (n,))
    return cursor.fetchall()

@database_common.connection_handler
def get_tags_for_question(cursor, question_id):
    query = """
            SELECT question_tag.question_id, question_tag.tag_id, tag.name
            FROM question_tag
            INNER JOIN tag ON question_tag.tag_id=tag.id
            WHERE question_tag.question_id = %s;"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_id(cursor, selected_tag):
    query = """
                SELECT id
                FROM tag
                WHERE name = %s
                """
    cursor.execute(query, (selected_tag,))
    return cursor.fetchall()

@database_common.connection_handler
def add_tag_to_question(cursor, selected_tag_id, question_id):
    query = """
                INSERT INTO question_tag
                VALUES(%s, %s)
                """
    cursor.execute(query, (question_id, selected_tag_id))

@database_common.connection_handler
def sign_user(cursor, username, email, hashed_password, time):
    query = """
    INSERT INTO users (username, email, hashed_password, register_time)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (username, email, hashed_password, time))


@database_common.connection_handler
def get_users(cursor):
    query = """
    SELECT id, username, email, register_time
    FROM users
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_user(cursor, id):
    query = """
    DELETE
    FROM users
    WHERE id = %s
    """
    cursor.execute(query, (id,))


@database_common.connection_handler
def get_hashed_password(cursor, username):
    query = """
    SELECT hashed_password
    FROM users
    WHERE username = %s
    """
    cursor.execute(query, (username,))
    return cursor.fetchall()


@database_common.connection_handler
def check_username(cursor, username):
    query = """
    SELECT username
    FROM users
    WHERE username = %s
    """
    cursor.execute(query, (username,))
    if cursor.fetchone() is None:
        return 0
    return 1
