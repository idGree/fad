# app/modules/user/views.py
"""
Модуль с пользовательскими классами для страницы пользователей.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from app.modules.user.models import User
from utils.decorators import admin_required
from app.db import db

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/')
@login_required
@admin_required  # Применяем наш декоратор
def user():
    title = 'User'
    user_items = User.query.all()
    return render_template('member/user/index.html', title=title, user_items=user_items)
