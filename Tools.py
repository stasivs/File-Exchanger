import random

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError


def create_url(len=25):
    url = ""
    for i in range(len):
        url += random.choice(alphabet)
    return url


alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(ord("a"), ord("z") + 1):
    alphabet.append(chr(i))
    alphabet.append(chr(i).upper())


def length(max_len):
    message = "Длина не должна превышать {} символов".format(max_len)

    def _length(form, field):
        if field.data > max_len:
            raise ValidationError(message)

    return _length


def check_password(password):
    message = ""


def check_username(username):
    message = ""


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired("Введите логин")])
    password = PasswordField('Пароль', validators=[DataRequired("Введите пароль")])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired("Введите логин"), length(20)])
    password = PasswordField('Пароль', validators=[DataRequired("Введите пароль"),
                                                   EqualTo('repeat_password', message='Пароли не совпадают')])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class AddArchive(FlaskForm):
    title = StringField('Заголовок', validators=[length(50)])
    info = TextAreaField('Описание', validators=[length(1000)])
    file = FileField(validators=[DataRequired()])
    submit = SubmitField('Добавить')
