from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
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