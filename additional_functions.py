import datetime
import os


def create_name_file(file_name):
    seconds_since_epoch = str(datetime.datetime.now().timestamp()).replace(".", '')
    file_type = file_name[-3:]
    file_name = file_name.replace("." + file_type, "")
    img_name = ''.join(filter(str.isalnum, file_name))
    return f'{img_name}{str(seconds_since_epoch)}.{file_type}'


def get_index(list_to_check):
    if len(list_to_check) == 0:
        return 0
    last_id = list_to_check[-1]['id']
    new_id = str(int(last_id) + 1)
    return new_id


def file_operation(file_list):
    if file_list.filename != "":
        file_name = create_name_file(file_list.filename)
        file_list.save(os.path.join('static', file_name))
        return file_name
    return "img.png"


def vote(questions, id, direction):
    for item in questions:
        if item['id'] == id:
            item['vote_number'] = str(int(item['vote_number']) + direction)
    return questions