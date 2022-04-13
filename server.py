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
    data = data_handler.get_questions()
    for item in data:
        if item["id"] == question_id:
            question_id = item
    return render_template("details.html", questions = question_details)

if __name__ == "__main__":
    app.run()
