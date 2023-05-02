"""app that stores passwords hashed with Bcrypt"""

import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret to everyone"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

SESSION_USER_KEY = "username"

@app.get("/")
def homepage():
    """Redirect to the register page"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Display register user form and submit the credentials"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session[SESSION_USER_KEY] = user.username

        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """
    Display login form and authenticate user ; flash error if unable
    to authenticate
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session[SESSION_USER_KEY] = user.username
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def user_info(username):
    """Display user information"""

    if SESSION_USER_KEY not in session or username != session[SESSION_USER_KEY]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    return render_template("user.html", user=user, form=form)


@app.post("/logout")
def logout_user():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")

@app.post("/users/<username>/delete")
def delete_user(username):
    """
    Delete the user from the database ; log the user out and redirect to
    homepage
    """

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()

    return redirect("/")