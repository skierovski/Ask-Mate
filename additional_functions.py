import datetime


def create_name_file(string):
    seconds_since_epoch = str(datetime.datetime.now().timestamp()).replace(".", '')
    file_type = string[-3:]
    string = string.replace("." + file_type, "")
    img_name = ''.join(filter(str.isalnum, string))
    img_name = img_name + str(seconds_since_epoch) + "." + file_type
    return img_name
