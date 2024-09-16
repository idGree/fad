# app/modules/profile/views.py
"""
Модуль с пользовательскими классами для страницы профиля пользователя.

После авторизации пользователя перенаправляем на страницу профиля.
Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template
from flask_login import login_required

# Создаем Blueprint для модуля profile с префиксом '/profile'
blueprint = Blueprint('profile', __name__, url_prefix='/profile')


@blueprint.route('/')
@login_required
def profile():
    """
    Страница профиля пользователя.

    Этот маршрут отображает основную информацию о профиле текущего
    аутентифицированного пользователя.

    :return: HTML-код страницы профиля пользователя.
    :rtype: str
    """
    title = 'Профиль'
    return render_template('member/profile.html', title=title)