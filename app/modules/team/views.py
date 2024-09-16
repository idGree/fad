# app/modules/team/views.py
"""
Модуль с пользовательскими классами для страницы с командами.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('team', __name__, url_prefix='/team')


@blueprint.route('/')
@login_required
def team():
    title = 'team'
    return render_template('member/team/index.html', title=title)