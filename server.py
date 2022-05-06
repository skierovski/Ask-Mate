import datetime
from flask import Flask, render_template, request, redirect, url_for
import data_handler
import additional_functions
import templates
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024


@app.route('/list')
def route_list():
    questions = data_handler.get_questions()
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
    return render_template('list.html', user_question=questions)


@app.route('/question/<q_id>')
def view_question(q_id):
    select_question = data_handler.get_question(q_id)
    select_answer = data_handler.get_answer(q_id)
    select_question_comments = data_handler.get_question_comments(q_id)
    select_answer_comments = data_handler.get_answer_comments(q_id)
    select_question_tag = data_handler.get_tags_for_question(q_id)
    return render_template('question.html', selected_question=select_question,
                           selected_answer=select_answer,
                           selected_question_comments=select_question_comments,
                           selected_answer_comments=select_answer_comments,
                           selected_question_tag=select_question_tag)


@app.route('/add-question', methods=['POST', 'GET'])
def add_new_question():
    if request.method == "GET":
        return render_template('newquestion.html')
    data_handler.add_question()
    new_question_index = data_handler.get_last_id()
    return redirect(f"/question/{str(new_question_index[0]['max'])}")


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == "GET":
        return render_template('newanswer.html', question_id=question_id)
    data_handler.add_answer(question_id)
    return redirect(f"/question/{str(question_id)}")


@app.route('/question/<q_id>/delete')
def delete_question(q_id):
    data_handler.delete_question(q_id)
    return redirect("/list")


@app.route('/question/<q_id>/edit', methods=['POST', 'GET'])
def edit_question(q_id):
    if request.method == 'GET':
        select_question = data_handler.get_question(q_id)
        return render_template('editquestion.html', selected_question=select_question)

    data_handler.update_question(q_id)
    return redirect(f"/question/{str(q_id)}")


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    q_id = data_handler.get_id(int(answer_id))
    data_handler.delete_answer(answer_id)
    return redirect(f"/question/{str(q_id[0]['question_id'])}")


@app.route('/question/<question_id>/<vote>')
def vote_question(question_id, vote):
    direction = 1 if vote == 'vote-up' else -1
    data_handler.vote('question', direction, question_id)
    return redirect("/list")


@app.route('/answer/<answer_id>/<vote>')
def vote_answer(answer_id, vote):
    direction = 1 if vote == 'vote-up' else -1
    data_handler.vote('answer', direction, answer_id)
    question_id = data_handler.get_id(int(answer_id))
    return redirect(f"/question/{str(question_id[0]['question_id'])}")


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def add_question_comment(question_id):
    if request.method == "GET":
        return render_template('newcomment.html', question_id=question_id)
    data_handler.add_question_comment(question_id)
    return redirect(f"/question/{str(question_id)}")


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_answer_comment(answer_id):
    if request.method == "GET":
        return render_template('new_answer_comment.html', answer_id=answer_id)
    question_id = data_handler.get_id(int(answer_id))
    data_handler.add_answer_comment(answer_id,question_id)
    return redirect(f"/question/{str(question_id[0]['question_id'])}")


@app.route('/search', methods=['POST', 'GET'])
def search():
    search_phrase = request.args.get('q')
    questions = data_handler.search_question(search_phrase)
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
    return render_template('list.html', user_question=questions)


@app.route('/answer/<a_id>/edit', methods=['POST', 'GET'])
def edit_answer(a_id):
    if request.method == 'GET':
        select_answer = data_handler.get_answer_to_edit(a_id)
        return render_template('editanswer.html', selected_answer=select_answer)

    q_id = data_handler.get_id(a_id)
    data_handler.update_answer(a_id)
    return redirect(f"/question/{str(q_id[0]['question_id'])}")


@app.route('/comment/<c_id>/edit', methods=['POST', 'GET'])
def edit_comment(c_id):
    if request.method == 'GET':
        select_comment = data_handler.get_comment_to_edit(c_id)
        return render_template('editcomment.html', selected_comment=select_comment)

    q_id = data_handler.get_q_id_from_comment(c_id)
    data_handler.update_comment(c_id)
    return redirect(f"/question/{str(q_id[0]['question_id'])}")


@app.route('/comments/<comment_id>/delete', methods=['POST', 'GET'])
def delete_comment(comment_id):
    q_id = data_handler.get_q_id_from_comment(comment_id)
    data_handler.delete_comment(comment_id)
    return redirect(f"/question/{str(q_id[0]['question_id'])}")


@app.route("/")
def last_question_list():
    questions = data_handler.get_n_last_question(5)
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
    return render_template('lastquestion.html', user_question=questions)


if __name__ == "__main__":
    app.run()
