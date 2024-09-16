# app/modules/team_set/views.py
"""
Модуль с пользовательскими классами для страницы с составом команд.
Из справочника сотрудников и справочника команд формируем состав каждой команды.
Один сотрудник может состоять в нескольких командах.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template

blueprint = Blueprint('team_set', __name__, url_prefix='/team_set')


@blueprint.route('/')
def team_set():
    title = 'team_set'
    return render_template('member/team_set/index.html', title=title)