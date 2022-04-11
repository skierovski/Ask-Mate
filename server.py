from flask import Flask, render_template

import data_handler

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/questions")
def questions():
    user_questions = data_handler.get_questions()
    return render_template('list.html', questions = user_questions)

@app.route("/questions/<question_id>")
def question_details(question_id):
    questions = data_handler.get_questions()
    for item in questions:
        if item["id"] == question_id:
            question = item
    return render_template("deatails.html", selected_question = question)

if __name__ == "__main__":
    app.run()
