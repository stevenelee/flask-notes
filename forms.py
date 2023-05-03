from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired()]
        )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
        )

    email = EmailField(
        "E-mail",
        validators=[InputRequired()]
        )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
        )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired()]
        )


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField(
        "Username",
        validators=[InputRequired()]
        )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
        )


class NoteForm(FlaskForm):
    """Form for adding a note"""

    title = StringField(
        "Title",
         validators=[InputRequired()]
    )

    content = TextAreaField(
        "Content",
         validators=[InputRequired()]
    )
#TODO: match length validators eg. Length(max=100)

"""TODO: make note edit form class that inherits noteform NoteEditForm(NoteForm)
"""

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""