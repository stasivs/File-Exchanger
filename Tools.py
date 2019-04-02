import random
import hashlib

from DB import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length


def create_url(len=25):
    url = ""
    for i in range(len):
        url += random.choice(alphabet)
    return url


alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(ord("a"), ord("z") + 1):
    alphabet.append(chr(i))
    alphabet.append(chr(i).upper())


def check_username(form, field):
    message = "Неверный логин"
    username = field.data

    if not UserModel(db.get_connection()).get(username):
        raise ValidationError(message)


def exist_username(form, field):
    message = "Пользователь с таким никнеймом уже существует"
    username = field.data

    if UserModel(db.get_connection()).get(username):
        raise ValidationError(message)


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired("Введите логин"), check_username])
    password = PasswordField('Пароль', validators=[DataRequired("Введите пароль")])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired("Введите логин"),
                                                Length(max=20, message="Кол-во символов не должно превышать 20"), exist_username])
    password = PasswordField('Пароль', validators=[DataRequired("Введите пароль"),
                                                   EqualTo('repeat_password', message='Пароли не совпадают')])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class AddFile(FlaskForm):
    title = StringField('Заголовок', validators=[Length(max=50, message="Кол-во символов не должно превышать 50")])
    info = TextAreaField('Описание', validators=[Length(max=1000, message="Кол-во символов не должно превышать 1000")])
    file = FileField(validators=[DataRequired("Вы не выбрали файл")])
    submit = SubmitField('Добавить')


class AddFolder(FlaskForm):
    title = StringField('Название папки', validators=[Length(max=50, message="Кол-во символов не должно превышать 50"),
                                                 DataRequired("Введите название папки")])
    submit = SubmitField('Создать')