from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from utils.logging import log_and_flash

def admin_required(f):
    """
    Декоратор для ограничения доступа к маршруту только для администраторов.

    :param f: Функция представления, которую нужно защитить.
    :return: Обернутая функция представления.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            # Если пользователь не авторизован, перенаправляем его на страницу входа
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            # Если пользователь не администратор, возвращаем отказ в доступе
            log_and_flash('У вас нет прав доступа к этой странице.', 'warning')
            return redirect(url_for('index.index'))  # Перенаправляем на главную страницу или другую
        return f(*args, **kwargs)

    return decorated_function
