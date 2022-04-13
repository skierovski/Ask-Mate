import datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import data_handler
import additional_functions

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024

templates_question = {
    'id': "",
    'submission_time': "",
    'view_number': "0",
    'vote_number': "0",
    'title': "",
    'message': "",
    'image': "img.png"
}

templates_answer = {
    'id': "",
    'submission_time': "",
    'vote_number': "0",
    'question_id': "",
    'message': "",
    'image': "img.png"
}

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/list')
def route_list():
    questions = data_handler.get_all_question()
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
    return render_template('list.html', user_question=questions)


@app.route('/question/<q_id>')
def view_question(q_id):
    select_question = data_handler.get_all_question(q_id)
    select_answer = data_handler.get_all_answer(q_id)
    return render_template('question.html', selected_question=select_question, selected_answer=select_answer)


@app.route('/add-question', methods=['POST', 'GET'])
def add_new_question():
    if request.method == "GET":
        return render_template('newquestion.html')
    if request.method == "POST":
        new_question = templates_question.copy()
        question = data_handler.get_all_question()
        if len(question)==0:
            new_question['id'] = "0"
        else:
            last_id = question[-1]['id']
            new_question['id'] = str(int(last_id) + 1)
        new_question['submission_time'] = str(datetime.datetime.now().strftime("%d/%m/%y %H:%M"))
        if 'title' in request.form:
            new_question['title'] = request.form['title']
        if 'message' in request.form:
            new_question['message'] = request.form['message']
        f = request.files['file']
        if f.filename != "":
            file_name = additional_functions.create_name_file(f.filename)
            new_question['image'] = file_name
            f.save(os.path.join('static', file_name))
        question.append(new_question)
        data_handler.write_table_to_file_question(data_handler.create_list_to_write(question))
        link_direct = "/question/" + str(new_question['id'])
    return redirect(link_direct)


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == "GET":
        return render_template('newanswer.html', question_id=question_id)
    if request.method == "POST":
        answer = data_handler.get_all_answer()
        new_answer = templates_answer.copy()
        if len(answer) == 0:
            new_answer['id'] = 0
        else:
            last_id = answer[-1]['id']
            new_answer['id'] = str(int(last_id) + 1)
        new_answer['submission_time'] = str(datetime.datetime.now().strftime("%d/%m/%y %H:%M"))
        new_answer['question_id'] = question_id
        if 'message' in request.form:
            new_answer['message'] = request.form['message']
        f = request.files['file_answer']
        if f.filename != "":
            file_name = additional_functions.create_name_file(f.filename)
            new_answer['image'] = file_name
            f.save(os.path.join('static', file_name))
        answer.append(new_answer)
        data_handler.write_table_to_file_answer(data_handler.create_list_to_write(answer))
        link_direct = "/question/" + str(question_id)
    return redirect(link_direct)


@app.route('/question/<q_id>/delete')
def delete_question(q_id):
    question = data_handler.get_all_question()
    for item in question:
        if item['id'] == str(q_id):
            question.remove(item)
    data_handler.write_table_to_file_question(data_handler.create_list_to_write(question))
    return redirect("/list")

@app.route('/question/<q_id>/edit',methods=['POST', 'GET'])
def edit_question(q_id):
    if request.method=='GET':
        select_question = data_handler.get_all_question(q_id)
        return render_template('editquestion.html', selected_question=select_question)
    if request.method =='POST':
        questions = data_handler.get_all_question()
        if 'title' in request.form:
            questions[int(q_id)]['title'] = request.form['title']
        if 'message' in request.form:
            questions[int(q_id)]['message'] = request.form['message']
        data_handler.write_table_to_file_question(data_handler.create_list_to_write(questions))
        link_direct = "/question/" + str(q_id)
        return redirect(link_direct)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answers = data_handler.get_all_answer()
    question_id=""
    for item in answers:
        if item['id'] == str(answer_id):
            question_id=item['question_id']
            answers.remove(item)
    data_handler.write_table_to_file_answer(data_handler.create_list_to_write(answers))
    link_direct = "/question/" + str(question_id)
    return redirect(link_direct)


@app.route('/question/<question_id>/<vote>')
def vote_question(question_id, vote):
    questions = data_handler.get_all_question()
    if vote == 'vote-up':
        for item in questions:
            if item['id']==question_id:
                item['vote_number']= str(int(item['vote_number'])+1)
    elif vote == 'vote-down':
        for item in questions:
            if item['id'] == question_id:
                item['vote_number'] = str(int(item['vote_number']) + 1)
    data_handler.write_table_to_file_question(data_handler.create_list_to_write(questions))
    return redirect("/list")


@app.route('/answer/<answer_id>/<vote>')
def vote_answer(answer_id, vote):
    answers = data_handler.get_all_answer()
    question_id= ''
    if vote == 'vote-up':
        for item in answers:
            if item['id']==answer_id:
                question_id = item['question_id']
                item['vote_number']= str(int(item['vote_number'])+1)
    elif vote == 'vote-down':
        for item in answers:
            if item['id']==answer_id:
                question_id = item['question_id']
                item['vote_number']= str(int(item['vote_number'])-1)
    data_handler.write_table_to_file_answer(data_handler.create_list_to_write(answers))
    link_direct = "/question/" + str(question_id)
    return redirect(link_direct)


if __name__ == "__main__":
    app.run()
