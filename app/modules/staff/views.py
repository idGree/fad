# app/modules/staff/views.py
"""
Модуль с пользовательскими классами для страницы с сотрудниками компании.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from app.modules.staff.models import Staff
from app.db import db

blueprint = Blueprint('staff', __name__, url_prefix='/staff')


@blueprint.route('/')
@login_required
def staff():
    title = 'Сотрудники'
    # Загружаем всех сотрудников с подгрузкой связанных записей TeamSet
    staff_items = Staff.query.options(
        db.joinedload(Staff.team_sets)  # Подгружаем связанные записи из TeamSet
    ).all()
    return render_template('member/staff/index.html', title=title, staff_items=staff_items)
