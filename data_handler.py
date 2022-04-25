import database_common


@database_common.connection_handler
def get_questions(cursor):
    query = """
            SELECT submission_time, view_number, vote_number, title, message, image
            FROM question
            ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_answers(cursor):
    query = """
           SELECT id, submission_time, vote_number, question_id, message, image
           FROM answer
           ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


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
