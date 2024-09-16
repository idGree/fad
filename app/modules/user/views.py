# app/modules/user/views.py
"""
Модуль с пользовательскими классами для страницы пользователей.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/')
@login_required
def user():
    title = 'User'
    return render_template('member/user/index.html', title=title)
