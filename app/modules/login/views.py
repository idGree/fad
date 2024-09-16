# app/modules/login/views.py
"""
Маршруты и обработчики запросов для модуля авторизации.

Этот модуль содержит маршруты для входа и выхода пользователя из системы.
Функция входа проверяет учетные данные пользователя и аутентифицирует его.
Функция выхода завершает сессию пользователя.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_user, logout_user, login_required

from app.modules.login.forms import LoginForm
from app.modules.user.models import User

# Создаем Blueprint для модуля login с префиксом '/login'
blueprint = Blueprint('login', __name__, url_prefix='/login')


@blueprint.route('/', methods=['GET', 'POST'])
def login():
    """
    Обрабатывает запросы на авторизацию пользователя.

    Если пользователь уже аутентифицирован, его перенаправляют на главную страницу.
    Если авторизация прошла успешно, пользователя перенаправляют на страницу профиля.
    В случае неудачной попытки входа выводится сообщение об ошибке.

    :return: Сгенерированный HTML-код страницы авторизации или редирект на другую страницу.
    :rtype: str
    """
    if current_user.is_authenticated:
        current_app.logger.info('Пользователь уже авторизованы')
        flash('Пользователь уже авторизованы!', 'info')
        return redirect(url_for('index.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            # Логирование неудачной попытки входа
            current_app.logger.warning('Неудачная попытка входа: неправильный логин или пароль')
            flash('Не корректный логин или пароль!', 'danger')
            return redirect(url_for('login.login'))

        login_user(user, remember=form.remember_me.data)

        # Логирование успешной авторизации
        current_app.logger.info(f'Успешная авторизация пользователя {user.user_email}')
        flash('Вы успешно вошли в систему!', 'success')
        return redirect(url_for('profile.profile'))

    # Обработка ошибок валидации формы
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Ошибка в поле {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('member/login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    """
    Обрабатывает выход пользователя из системы.

    Завершает текущую сессию пользователя и перенаправляет его на главную страницу.

    :return: Перенаправление на главную страницу.
    :rtype: werkzeug.wrappers.Response
    """
    current_app.logger.info(f'Пользователь {current_user.user_email} вышел из системы')
    logout_user()
    return redirect(url_for('index.index'))
