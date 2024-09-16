# app/modules/login/forms.py
"""
Формы для модуля авторизации.

Этот модуль содержит форму для авторизации пользователя в системе.
Форма включает в себя поля для ввода адреса электронной почты, пароля,
а также опцию "Запомнить меня".
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """
    Форма для авторизации пользователя в систему.

    :param email: Поле для ввода адреса электронной почты.
    :type email: StringField
    :param password: Поле для ввода пароля.
    :type password: PasswordField
    :param remember_me: Поле для выбора опции "Запомнить меня".
    :type remember_me: BooleanField
    :param submit: Кнопка для отправки формы.
    :type submit: SubmitField
    """
    email = StringField(
        'Почта: ',
        validators=[DataRequired(), Email(message="Введите корректный email-адрес.")],
        render_kw={'class': 'form-control', 'id': 'email', 'type': 'email'},
    )
    password = PasswordField(
        'Пароль: ',
        validators=[DataRequired(message="Поле пароля обязательно для заполнения.")],
        render_kw={'class': 'form-control', 'type': 'password', 'id': 'password'},
    )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={'class': 'form-check-input', 'type': 'checkbox'}
    )
    submit = SubmitField(
        'Войти',
        render_kw={'class': 'btn btn-primary'},
    )
