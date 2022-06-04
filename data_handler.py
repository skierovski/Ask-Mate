from flask import request
import additional_functions
import database_common


@database_common.connection_handler
def get_questions(cursor):
    query = """
            SELECT question.*, users.username AS author
            FROM question
            INNER JOIN users  ON users.id = question.user_id
            ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor, q_id):
    query = """
            SELECT question.*, users.username AS author
            FROM question
            INNER JOIN users  ON users.id = question.user_id
            WHERE question.id = %s
            ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_answer(cursor, q_id):
    query = """
           SELECT answer.*,users.username AS author
           FROM answer
           INNER JOIN users  ON users.id = answer.user_id
           WHERE answer.question_id = %s
           ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor):
    query = """
           SELECT answer.*,users.username AS author
           FROM answer
           INNER JOIN users  ON users.id = answer.user_id"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor, author_id):
    new_title = request.form.get('title', default="")
    new_message = request.form.get('ckeditor')
    upload_file = request.files['file']
    new_image = additional_functions.file_operation(upload_file)
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id) 
        VALUES (now(), 0, 0, %s, %s, %s, %s);    
    """
    cursor.execute(query, (new_title, new_message, new_image, author_id))


@database_common.connection_handler
def get_last_id(cursor):
    query = """
            SELECT max(id) FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_answer(cursor, question_id, author_id):
    new_message = request.form.get('ckeditor')
    upload_file = request.files['file_answer']
    new_image = additional_functions.file_operation(upload_file)
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id) 
        VALUES (now(), 0, %s, %s, %s, %s);    
    """
    cursor.execute(query, (question_id, new_message, new_image, author_id))


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id= %s;
    """
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def update_question(cursor, question_id):
    new_title = request.form.get('title', default="")
    new_message = request.form.get('ckeditor')
    query = """
        UPDATE question 
        SET title= %s, message =%s
     WHERE id = %s;
    """
    cursor.execute(query, (new_title,new_message,question_id))


@database_common.connection_handler
def update_view_number(cursor, q_id):
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %s
    """
    cursor.execute(query, (q_id,))


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
           DELETE
           FROM answer
           WHERE id = %s"""
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
           SELECT comment.*, users.username AS author
           FROM comment
           INNER JOIN users  ON users.id = comment.user_id
           WHERE comment.question_id = %s AND comment.answer_id is NULL 
           ORDER BY comment.submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()


@database_common.connection_handler
def add_question_comment(cursor, question_id, author_id):
    new_message = request.form.get('ckeditor')
    query = """
        INSERT INTO comment (question_id, message, submission_time, edited_count, user_id) 
        VALUES (%s, %s, now(), 0, %s);    
    """
    cursor.execute(query, (question_id, new_message, author_id))


@database_common.connection_handler
def get_answer_comments(cursor, question_id):
    query = """
           SELECT comment.*, users.username AS author
           FROM comment
           INNER JOIN users  ON users.id = comment.user_id
           WHERE comment.question_id = %s
           ORDER BY submission_time"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def add_answer_comment(cursor, answer_id, question_id, author_id):
    new_message = request.form.get('ckeditor')
    query = """
        INSERT INTO comment (question_id,answer_id, message, submission_time, edited_count, user_id) 
        VALUES (%s, %s, %s, now(), 0, %s);    
    """
    cursor.execute(query, (question_id, answer_id, new_message, author_id))


@database_common.connection_handler
def search_question(cursor, search_phrase):
    search_phrase = '%'+search_phrase+'%'
    query = """
            SELECT question.*,users.username AS author 
            FROM question
            INNER JOIN users  ON users.id = question.user_id
            WHERE question.title like %s  or question.message like %s   
        """
    cursor.execute(query, (search_phrase, search_phrase,))
    return cursor.fetchall()


@database_common.connection_handler
def search_answer(cursor, search_phrase):
    search_phrase = '%' + search_phrase + '%'
    query = """
            SELECT answer.*,users.username AS author 
            FROM answer
            INNER JOIN users  ON users.id = answer.user_id
            WHERE answer.message like %s   
        """
    cursor.execute(query, (search_phrase,))
    return cursor.fetchall()


@database_common.connection_handler
def update_answer(cursor, answer_id):
    new_message = request.form.get('ckeditor')
    query = """
        UPDATE answer 
        SET message =%s
        WHERE id = %s;
    """
    cursor.execute(query, (new_message, answer_id))


@database_common.connection_handler
def get_answer_to_edit(cursor, q_id):
    query = """
           SELECT *
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
    new_message = request.form.get('ckeditor')
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
           SELECT question.*,users.username AS author
           FROM question 
           INNER JOIN users  ON users.id = question.user_id
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
    return cursor.fetchone()


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
    return cursor.fetchall() # fetchone


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


@database_common.connection_handler
def get_user_id(cursor, username):
    query = """
    SELECT id
    FROM users
    WHERE username = %s
    """
    cursor.execute(query, (username,))
    return cursor.fetchone()


@database_common.connection_handler
def get_user_username_and_reputation(cursor, user_id):
    query = """
    SELECT username, reputation
    FROM users
    WHERE id = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def user_data_question(cursor, user_id):
    query = """
        SELECT *
        FROM question
        WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

@database_common.connection_handler
def user_data_answer(cursor, user_id):
    query = """
            SELECT *
            FROM answer
            WHERE user_id = %s
        """

    cursor.execute(query, (user_id,))
    return cursor.fetchall()



@database_common.connection_handler
def user_data_comment(cursor, user_id):
    query = """
            SELECT *
            FROM comment
            WHERE user_id = %s
        """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

@database_common.connection_handler
def check_if_tag_in_tags(cursor, selected_tag):
    query = """
    SELECT id
    FROM tag
    WHERE name = %s
    """
    cursor.execute(query, (selected_tag,))
    if cursor.fetchone() is None:
        return 0
    return 1


@database_common.connection_handler
def add_new_tag_to_base(cursor, selected_tag):
    query = """
    INSERT INTO tag (name)
    VALUES(%s)
    """
    cursor.execute(query, (selected_tag,))


@database_common.connection_handler
def get_tags(cursor):
    query = """
    SELECT *
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag(cursor, question_id, tag_id):
    query = """
    DELETE
    FROM question_tag
    WHERE question_id = %s and tag_id = %s
    """
    cursor.execute(query, (question_id, tag_id))

@database_common.connection_handler
def accept_answer(cursor, answer_id):
    query = """
        UPDATE answer 
        SET accepted = 1
        WHERE id = %s;
    
    """
    cursor.execute(query, (answer_id,))

@database_common.connection_handler
def declined_answer(cursor, answer_id):
    query = """
            UPDATE answer 
            SET accepted = 0
            WHERE id = %s;

        """
    cursor.execute(query, (answer_id,))

@database_common.connection_handler
def get_user_id_from_answer_id(cursor, answer_id):
    query = """
        SELECT user_id
        FROM answer
        WHERE id = %s
    """
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()

@database_common.connection_handler
def reputation_answer_up(cursor, user_id):
    query = """
        UPDATE users
        SET reputation = reputation +10
        WHERE id = %s;
    """
    cursor.execute(query, (user_id,))


@database_common.connection_handler
def reputation_answer_down(cursor, user_id):
    query = """
        UPDATE users
        SET reputation = reputation -2
        WHERE id = %s;
        """
    cursor.execute(query, (user_id,))



@database_common.connection_handler
def get_user_id_from_question_id(cursor, question_id):
    query = """
        SELECT user_id
        FROM question
        WHERE id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchone()

@database_common.connection_handler
def reputation_question_up(cursor, user_id):
    query = """
        UPDATE users
        SET reputation = reputation +5
        WHERE id = %s;
    """
    cursor.execute(query, (user_id,))


@database_common.connection_handler
def reputation_question_down(cursor, user_id):
    query = """
        UPDATE users
        SET reputation = reputation -2
        WHERE id = %s;
        """
    cursor.execute(query, (user_id,))

@database_common.connection_handler
def reputation_accepted_up(cursor, user_id):
    query = """
        UPDATE users
        SET reputation = reputation +15
        WHERE id = %s;
    """
    cursor.execute(query, (user_id,))


@database_common.connection_handler
def get_question_id_by_tag_id(cursor, tag_id):
    query = """
    SELECT question_id
    FROM question_tag
    WHERE tag_id = %s
    """
    cursor.execute(query, (tag_id,))
    return cursor.fetchall()
