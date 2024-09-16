# app/modules/team_set/models.py
"""
Модуль для определения модели данных User в приложении Flask.

Этот модуль содержит модель пользователя, которая используется для
хранения и управления информацией о пользователях, включая их имя,
электронную почту, хэшированный пароль и роль. Модель интегрирована
с Flask-Login для обеспечения функций аутентификации.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """
        Устанавливает хэшированный пароль пользователя.

        :param str password: Пароль, который необходимо захэшировать и сохранить.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Проверяет пароль пользователя на соответствие хешу.

        :param str password: Пароль для проверки.
        :return: Возвращает True, если пароль корректен, иначе False.
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(id={self.id}, user_name={self.user_name})>"
