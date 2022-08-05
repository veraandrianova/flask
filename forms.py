from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired, ValidationError


class LoginForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=2, max=100)])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=2, max=100)])
    phone = StringField("Телефон: ")
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=3, max=100)])
    psw_2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField("Зарегистрироваться")


class PasswordChange(FlaskForm):
    phone = StringField("Телефон: ")
    psw = PasswordField("Новый пароль: ", validators=[DataRequired(), Length(min=3, max=100)])
    psw_2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField("Поменять пароль")


class CreatePosts(FlaskForm):
    title = StringField("Название статьи: ", validators=[Length(min=3, max=100)])
    body = TextAreaField("Текст: ", validators=[Length(min=3, max=10000)])
    submit = SubmitField("Загрузить")
