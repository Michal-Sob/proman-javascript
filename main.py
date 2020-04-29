from flask import Flask, render_template, url_for, request, session, redirect
from util import json_response, is_logged_in, session_username
import data_handler
from os import urandom
import persistence

app = Flask(__name__)
app.secret_key = urandom(16).hex()


@app.route("/")
def index():
    """
    This is a one-pager which shows all the boards and cards
    """
    return render_template('index.html', logged_in=is_logged_in(), username=session_username())


@app.route("/get-boards")
@json_response
def get_boards():
    """
    All the boards
    """
    return data_handler.get_boards()


@app.route("/get-cards/<int:board_id>")
@json_response
def get_cards_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    return data_handler.get_cards_for_board(board_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    wrong_data = None
    if request.method == "POST":
        print(request.form["password"])
        session["username"] = request.form["username"]
        if data_handler.verify_password(request.form["password"], persistence.get_user(session["username"])):
            return redirect("/")
        else:
            session.pop("username", None)
            wrong_data = "Invalid user name or password  "
            return render_template('login&&registration_form.html', wrong_data=wrong_data, action="login", submit="Login")

    return render_template("login&&registration_form.html", logged_in=is_logged_in(), wrong_data=wrong_data,
                                                            submit="Login", action="login")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        new_user = request.form
        data_handler.new_user(new_user)

    return render_template("login&&registration_form.html", submit="Registration", action="registration")


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
