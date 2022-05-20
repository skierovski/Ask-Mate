import datetime
from flask import Flask, render_template, request, redirect, session, url_for
import data_handler
import bcrypt
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)
app.secret_key = b'abc'
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024


def colored_text(text, search_phrase):
    return text.replace(search_phrase, search_phrase.upper())


@app.route('/')
@app.route('/list')
def route_list():
    is_log_in = False
    questions = data_handler.get_questions()
    if "username" in session:
        is_log_in = True
        order_direction = request.args.get("order_direction", "desc")
        order_by = request.args.get("order_by", "title")
        questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
        user_id = data_handler.get_user_id(session['username'])['id']
        user_username = data_handler.get_user_username_and_reputation(user_id)
        return render_template('list.html', user_question=questions, is_log_in=is_log_in, user_id=user_id, user_username=user_username)
    return render_template('list.html', user_question=questions, is_log_in=is_log_in)


@app.route('/question/<q_id>')
def view_question(q_id):
    user_id = 0
    is_log_in = False
    if "username" in session:
        is_log_in = True
    if 'username' in session:
        user_id = data_handler.get_user_id(session['username'])['id']
    data_handler.update_view_number(q_id)
    select_question = data_handler.get_question(q_id)
    select_answer = data_handler.get_answer(q_id)
    select_question_comments = data_handler.get_question_comments(q_id)
    select_answer_comments = data_handler.get_answer_comments(q_id)
    select_question_tag = data_handler.get_tags_for_question(q_id)
    return render_template('question.html', selected_question=select_question,
                           selected_answer=select_answer,
                           selected_question_comments=select_question_comments,
                           selected_answer_comments=select_answer_comments,
                           selected_question_tag=select_question_tag,
                           is_log_in=is_log_in,
                           user_id=user_id)


@app.route('/add-question', methods=['POST', 'GET'])
def add_new_question():
    author_id = data_handler.get_user_id(session['username'])['id']
    if request.method == "GET":
        return render_template('newquestion.html')
    data_handler.add_question(author_id)
    new_question_index = data_handler.get_last_id()
    return redirect(f"/question/{str(new_question_index[0]['max'])}")


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    author_id = data_handler.get_user_id(session['username'])['id']
    if request.method == "GET":
        return render_template('newanswer.html', question_id=question_id)
    data_handler.add_answer(question_id, author_id)
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
    user_id = data_handler.get_user_id_from_question_id(question_id)
    if direction == 1:
        data_handler.reputation_question_up(user_id['user_id'])
    else:
        data_handler.reputation_question_down(user_id['user_id'])
    data_handler.vote('question', direction, question_id)
    return redirect("/list")


@app.route('/answer/<answer_id>/<vote>')
def vote_answer(answer_id, vote):
    direction = 1 if vote == 'vote-up' else -1
    user_id = data_handler.get_user_id_from_answer_id(answer_id)
    if direction == 1:
        data_handler.reputation_answer_up(user_id['user_id'])
    else:
        data_handler.reputation_answer_down(user_id['user_id'])
    data_handler.vote('answer', direction, answer_id)
    question_id = data_handler.get_id(int(answer_id))
    return redirect(f"/question/{str(question_id[0]['question_id'])}")


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def add_question_comment(question_id):
    author_id = data_handler.get_user_id(session['username'])['id']
    if request.method == "GET":
        return render_template('newcomment.html', question_id=question_id)
    data_handler.add_question_comment(question_id, author_id)
    return redirect(f"/question/{str(question_id)}")


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_answer_comment(answer_id):
    author_id = data_handler.get_user_id(session['username'])['id']
    if request.method == "GET":
        return render_template('new_answer_comment.html', answer_id=answer_id)
    question_id = data_handler.get_id(answer_id)[0]['question_id']
    data_handler.add_answer_comment(answer_id, question_id, author_id)
    return redirect(f"/question/{str(question_id)}")


@app.route('/search', methods=['POST', 'GET'])
def search():
    search_phrase = request.args.get('q')
    questions = data_handler.search_question(search_phrase)
    answer = data_handler.search_answer(search_phrase)
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
    return render_template('search.html', user_question=questions, user_answer=answer, search_phrase=search_phrase)


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


@app.route("/latest_questions")
def last_question_list():
    is_log_in = False
    if "username" in session:
        is_log_in = True
    questions = data_handler.get_n_last_question(5)
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
    return render_template('lastquestion.html', user_question=questions, is_log_in=is_log_in)


@app.route('/question/<question_id>/new-tag', methods=['POST', 'GET'])
def add_tag(question_id):
    if request.method == 'GET':
        tags_available_to_add = []
        all_tags = []
        for i in range(len(data_handler.get_tags())):
            all_tags.append(data_handler.get_tags()[i]['name'])
        question_tags = []
        for i in range(len(data_handler.get_tags_for_question(question_id))):
            question_tags.append(data_handler.get_tags_for_question(question_id)[i]['name'])
        for tag in all_tags:
            if tag not in question_tags:
                tags_available_to_add.append(tag)
        return render_template('new_tag.html', question_id=question_id, tags=tags_available_to_add)
    selected_tag = request.form.get('tag')
    if data_handler.check_if_tag_in_tags(selected_tag) == 1:
        selected_tag_id = data_handler.get_tag_id(selected_tag)['id']
        data_handler.add_tag_to_question(selected_tag_id, question_id)
    else:
        data_handler.add_new_tag_to_base(selected_tag)
        selected_tag_id = data_handler.get_tag_id(selected_tag)['id']
        data_handler.add_tag_to_question(selected_tag_id, question_id)
    return redirect(f"/question/{str(question_id)}")


@app.route('/question/<question_id>/delete-tag', methods=['POST', 'GET'])
def delete_tag(question_id):
    if request.method == 'GET':
        question_tags = []
        for i in range(len(data_handler.get_tags_for_question(question_id))):
            question_tags.append(data_handler.get_tags_for_question(question_id)[i]['name'])
        return render_template('delete_tag.html', question_id=question_id, question_tags=question_tags)
    selected_tag_id = data_handler.get_tag_id(request.form.get('tag'))['id']
    data_handler.delete_tag(question_id, selected_tag_id)
    return redirect(f"/question/{str(question_id)}")


@app.route("/sign_up", methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template("sign_up.html")
    username = request.form.get('username')
    if data_handler.check_username(username) == 0:
        email = request.form.get('email')
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(request.form.get('password').encode('utf-8'), salt)
        time = datetime.datetime.now()
        data_handler.sign_user(username, email, password.decode('utf-8'), time)
        return render_template('/hello.html', user_name=username, email=email, password=password)
    else:
        return render_template('/sign_up.html', user_duplicated=True, username=username)


@app.route('/list_of_users', methods=['GET'])
def list_of_users():
    is_log_in = False
    if "username" in session:
        is_log_in = True
    all_users = data_handler.get_users()
    return render_template('list_of_users.html', all_users=all_users, is_log_in=is_log_in)


@app.route('/user/<user_id>/delete', methods=['GET'])
def delete_user(user_id):
    data_handler.delete_user(user_id)
    return redirect('/list_of_users')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if if_valid_username(username):
            password = request.form.get("password")
            hashed_password = data_handler.get_hashed_password(username)[0]['hashed_password'].encode('utf-8')
            if hashed_password is not None:
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    session['username'] = username
                    return redirect('/list')
            session['bad_login_or_password'] = True
            return redirect(url_for("login"))
    return render_template("login.html", status=session.get('bad_login_or_password', default=False))


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/list')


def if_valid_username(username):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(len(numbers)):
        if numbers[i] in list(username):
            return False
        return True


@app.route('/users/<user_id>', methods=['GET'])
def account_page(user_id):
    is_log_in = False
    if "username" in session:
        is_log_in = True
    user_content_question = data_handler.user_data_question(user_id)
    user_content_answer = data_handler.user_data_answer(user_id)
    user_content_comment = data_handler.user_data_comment(user_id)
    username = data_handler.get_user_username_and_reputation(user_id)
    return render_template("account_details.html", question=user_content_question,
                                                    answer=user_content_answer,
                                                    comment=user_content_comment,
                                                    is_log_in=is_log_in,
                                                    username=username)



@app.route('/answer/<answer_id>/accept')
def accept_answer(answer_id):
    q_id = data_handler.get_id(answer_id)
    user_id = data_handler.get_user_id_from_answer_id(answer_id)
    data_handler.reputation_accepted_up(user_id['user_id'])
    data_handler.accept_answer(answer_id)
    return redirect(f"/question/{str(q_id[0]['question_id'])}")


@app.route('/answer/<answer_id>/declined')
def decline_answer(answer_id):
    q_id = data_handler.get_id(answer_id)
    data_handler.declined_answer(answer_id)
    return redirect(f"/question/{str(q_id[0]['question_id'])}")


@app.route('/tag_page')
def tag_page():
    tags = data_handler.get_tags()
    return render_template('tag_page.html', tags=tags)


@app.route('/tag_page/<tag>')
def questions_tag_page(tag):
    questions = []
    questions_id = []
    if tag == 'c':
        tag = 'c#'
    tag_id = data_handler.get_tag_id(tag)['id']
    for i in range(len(data_handler.get_question_id_by_tag_id(tag_id))):
        questions_id.append(data_handler.get_question_id_by_tag_id(tag_id)[i]['question_id'])
    for id in questions_id:
        questions.append(data_handler.get_question(id))
    return render_template('question_tag_page.html', questions=questions, tag=tag)


if __name__ == "__main__":
    app.run()

