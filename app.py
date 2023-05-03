"""app that stores passwords hashed with Bcrypt"""

import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret to everyone"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

USER_KEY = "username"

@app.get("/")
def homepage():
    """Redirect to the register page"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Display register user form and submit the credentials."""

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

        session[USER_KEY] = user.username

        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """
    Display login form and authenticate user ; flash error if unable
    to authenticate.
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session[USER_KEY] = user.username
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def user_info(username):
    """Display user information."""

    if USER_KEY not in session or username != session[USER_KEY]:
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

"""TODO: FIND ALL NOTES IN DB AND DELETE THEM BEFORE"""

@app.post("/users/<username>/delete")
def delete_user(username):
    """
    Delete the user from the database ; log the user out and redirect to
    homepage.
    """

    if USER_KEY not in session or username != session[USER_KEY]:
        raise Unauthorized()

    form = CSRFProtectForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)

        Note.query.filter_by(owner_username=username).delete()

        db.session.delete(user)
        db.session.commit()

        session.pop("username")

    return redirect("/")


"""TODO: USE COMMENT SEPARATORS WITH #
         KEEP CONSISTENT ORDER OF ROUTES
"""

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_notes(username):
    """Display form to add note ; add note and redirect to user page."""

    if USER_KEY not in session or username != session[USER_KEY]:
        raise Unauthorized()

    form = NoteForm()
    User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title,
                    content=content,
                    owner_username=username)

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("add_note.html", form=form)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_notes(note_id):
    """Show edit note form, update note on submit."""

    note = Note.query.get_or_404(note_id)

    if USER_KEY not in session or note.owner_username != session[USER_KEY]:
        raise Unauthorized()

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        flash("Note updated!")
        return redirect(f"/users/{note.owner_username}")

    return render_template("edit_note.html", form=form, note=note)


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Delete note and redirect to user page."""

    note = Note.query.get_or_404(note_id)
    # user = note.user

    if USER_KEY not in session or note.owner_username != session[USER_KEY]:
        raise Unauthorized()

    form = CSRFProtectForm()


    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    """TODO: else, check for CSRF token """