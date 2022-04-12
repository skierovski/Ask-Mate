import datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import data_handler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/list')
def route_list():
    questions = data_handler.get_all_question()
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction=='desc'))
    return render_template('list.html', user_question=questions)


@app.route('/question/<q_id>')
def view_question(q_id):
    question = data_handler.get_all_question()
    answer = data_handler.get_all_answer()
    select_question = []
    select_answer = []
    for item in question:
        if item['id'] == q_id:
            select_question = item
    for item in answer:
        if item['question_id'] == q_id:
            select_answer.append(item)
    return render_template('question.html', selected_question=select_question, selected_answer=select_answer)


@app.route('/add-question', methods=['POST', 'GET'])
def add_new_question():
    if request.method == "GET":
        question = data_handler.get_all_question()
        last_id = question[-1]['id']
        new_id = int(last_id) + 1
        return render_template('newquestion.html')
    if request.method == "POST":
        new_question={}
        question = data_handler.get_all_question()
        last_id = question[-1]['id']
        new_question['id'] = str(int(last_id) + 1)
        new_question['submission_time'] = datetime.now()
        new_question['view_number'] = "0"
        # globalny pusty słownik
        new_question['vote_number'] = "0"
        if 'title' in request.form:
            new_question['title'] = request.form['title']
        if 'message' in request.form:
            new_question['message'] = request.form['message']
        f = request.files['file']
        if f.filename !="":
            new_question['image'] = f.filename
            filename = secure_filename(f.filename)
            f.save(os.path.join('static', filename))
        else:
            new_question['image'] = 'img.png'
        question.append(new_question)
        list_to_return = []
        for item in question:
            list_to_return.append(item.values())
        data_handler.write_table_to_file_question(list_to_return)
        link_direct="/question/"+str(int(last_id)+1)
    return redirect(link_direct)


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == "GET":
        return render_template('newanswer.html', question_id=question_id)
    if request.method == "POST":
        answer = data_handler.get_all_answer()
        select_answer = []
        new_answer={}
        if len(answer)==0:
            new_answer['id']=0
        else:
            last_id = answer[-1]['id']
            new_answer['id'] = str(int(last_id) + 1)
        new_answer['submission_time'] = "1493368154"
        new_answer['vote_number'] = "0"
        new_answer['question_id'] = question_id
        if 'message' in request.form:
            new_answer['message'] = request.form['message']
        new_answer['image'] = '""\n'
        answer.append(new_answer)
        list_to_return = []
        for item in answer:
            list_to_return.append(item.values())
        data_handler.write_table_to_file_answer(list_to_return)
        link_direct = "/question/" + str(question_id)
    return redirect(link_direct)


@app.route('/question/<q_id>/delete')
def delete_question(q_id):
    question = data_handler.get_all_question()
    answer = data_handler.get_all_answer()
    for item in question:
        if item['id'] == str(q_id):
            question.remove(item)
    list_to_return = []
    for item in question:
        list_to_return.append(item.values())
    data_handler.write_table_to_file_question(list_to_return)
    for item in answer:
        if item['question_id'] == str(q_id):
            answer.remove(item)
    list_answer_to_return=[]
    for item in answer:
        list_answer_to_return.append(item.values())
    data_handler.write_table_to_file_answer(list_answer_to_return)
    return redirect("/list")


if __name__ == "__main__":
    app.run()
