# app/modules/index/views.py
"""
Модуль с пользовательскими классами для главной страницы приложения.

Главная страница не спрятана за авторизацию и доступна всем пользователям.
Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template

# Создаем Blueprint для модуля index с префиксом '/index'
blueprint = Blueprint('index', __name__, url_prefix='/index')


@blueprint.route('/')
def index():
    """
    Главная страница приложения.

    Этот маршрут отображает главную страницу приложения и доступен
    как для авторизованных, так и для неавторизованных пользователей.

    :return: Сгенерированный HTML-код главной страницы.
    :rtype: str
    """
    title = 'Главная'
    return render_template('member/index.html', title=title)
