# app/modules/staff/views.py
"""
Модуль с пользовательскими классами для страницы с сотрудниками компании.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('staff', __name__, url_prefix='/staff')


@blueprint.route('/')
@login_required
def staff():
    title = 'Staff'
    return render_template('member/staff/index.html', title=title)
