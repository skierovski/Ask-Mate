from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/list')
def route_list():
    question = data_handler.get_all_question()
    return render_template('list.html', user_question=question)


@app.route('/question/<q_id>')
def edit_story(q_id):
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

@app.route('/add-question')
def add_new_question():
    question = data_handler.get_all_question()
    return render_template('list.html', user_question=question)


if __name__ == "__main__":
    app.run()
