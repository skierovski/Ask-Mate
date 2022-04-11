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


if __name__ == "__main__":
    app.run()
