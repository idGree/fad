# app/modules/staff/views.py
"""
Модуль с пользовательскими классами для страницы с сотрудниками компании.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template

blueprint = Blueprint('staff', __name__, url_prefix='/staff')


@blueprint.route('/')
def staff():
    title = 'Staff'
    return render_template('member/staff/index.html', title=title)
