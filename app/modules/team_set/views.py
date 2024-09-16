# app/modules/team_set/views.py
"""
Модуль с пользовательскими классами для страницы с составом команд.
Из справочника сотрудников и справочника команд формируем состав каждой команды.
Один сотрудник может состоять в нескольких командах.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from app.modules.team_set.models import TeamSet
from app.db import db

blueprint = Blueprint('team_set', __name__, url_prefix='/team_set')


@blueprint.route('/')
@login_required
def team_set():
    title = 'Состав команд'
    # Загружаем все записи из TeamSet с подгрузкой связанных команд и сотрудников
    team_set_items = TeamSet.query.options(
        db.joinedload(TeamSet.team),  # Подгружаем связанные данные из Team
        db.joinedload(TeamSet.staff)  # Подгружаем связанные данные из Staff
    ).all()

    return render_template('member/team_set/index.html', title=title, team_set_items=team_set_items)
