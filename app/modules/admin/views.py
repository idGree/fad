# app/modules/admin/views.py
"""
Модуль с пользовательскими классами для административной панели.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import redirect, request, url_for, render_template, current_app
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, AdminIndexView, expose
from sqlalchemy.exc import IntegrityError
from utils.logging import log_and_flash


class MyModelView(ModelView):
    """
        Класс для управления моделями через Flask-Admin.

        Этот класс настраивает доступ к страницам управления моделями в административной панели.
        Доступ разрешен только авторизованным пользователям с ролью 'admin'.

        Методы:
            is_accessible() -> bool:
                Проверяет, доступен ли данный интерфейс для текущего пользователя.

            inaccessible_callback(name: str, **kwargs):
                Перенаправляет на страницу входа, если доступ к панели запрещен.
        """

    # page_size = 100
    # action_disallowed_list = ['delete', ]
    # can_view_details = True  # show a modal dialog with records details

    def is_accessible(self):
        """
        Определяет, доступен ли данный интерфейс для текущего пользователя.

        Доступ разрешен только авторизованным пользователям с ролью 'admin'.

        :return: True, если пользователь авторизован и имеет роль 'admin', иначе False.
        :rtype: bool
        """
        if current_user.is_authenticated and current_user.role == 'admin':
            return True
        log_and_flash('Доступ к разделам админки вам запрещен!', 'danger')

        return False

    def inaccessible_callback(self, name, **kwargs):
        """
        Перенаправляет пользователя на страницу входа, если доступ запрещен.

        :param name: Имя вызванного действия.
        :type name: str
        :param kwargs: Дополнительные параметры.
        :return: Перенаправление на страницу входа.
        :rtype: werkzeug.wrappers.Response
        """
        return redirect(url_for('login.login', next=request.path))

    def is_action_allowed(self, name):
        """
        Проверяет, разрешены ли массовые действия (bulk actions). В данном случае все массовые действия отключены.

        :param name: Имя действия.
        :return: False, поскольку массовые действия не поддерживаются.
        :rtype: bool
        """
        return False

    def on_model_change(self, form, model, is_created):
        """
        Переопределение метода для логирования событий создания или изменения записи.

        :param form: Форма, используемая для создания или изменения записи.
        :param model: Модель, над которой проводится операция.
        :param is_created: Флаг, указывающий, была ли запись создана (True) или обновлена (False).
        :type form: FlaskForm
        :type model: SQLAlchemy модель
        :type is_created: bool
        """
        if is_created:
            current_app.logger.info(f'Запись {model} была успешно создана.')
        else:
            current_app.logger.info(f'Запись {model} была обновлена.')

    def after_model_delete(self, model):
        """
        Переопределение метода для логирования событий удаления записи.

        :param model: Модель, которая будет удалена.
        :type model: SQLAlchemy модель
        """
        current_app.logger.warning(f'Запись {model} была удалена.')



class MyAdminIndexView(AdminIndexView):
    """
        Класс для настройки главной страницы административной панели.

        Этот класс управляет доступом к главной странице панели Flask-Admin.
        Доступ разрешен только авторизованным пользователям с ролью 'admin'.

        Методы:
            is_accessible() -> bool:
                Проверяет, доступен ли данный интерфейс для текущего пользователя.

            inaccessible_callback(name: str, **kwargs):
                Перенаправляет на страницу входа, если доступ к панели запрещен.
        """

    def is_accessible(self):
        """
        Определяет, доступен ли данный интерфейс для текущего пользователя.

        Доступ разрешен только авторизованным пользователям с ролью 'admin'.

        :return: True, если пользователь авторизован и имеет роль 'admin', иначе False.
        :rtype: bool
        """
        if current_user.is_authenticated and current_user.role == 'admin':
            return True
        log_and_flash('Доступ в админку вам запрещен!', 'danger')
        return False

    def inaccessible_callback(self, name, **kwargs):
        """
        Перенаправляет пользователя на страницу входа, если доступ запрещен.

        :param name: Имя вызванного действия.
        :type name: str
        :param kwargs: Дополнительные параметры.
        :return: Перенаправление на страницу входа.
        :rtype: werkzeug.wrappers.Response
        """
        return redirect(url_for('login.login', next=request.path))

    @expose('/')
    def index(self):
        """
        Кастомная главная страница для административной панели.
        Отображает ссылки на справочники.
        """
        return self.render('admin/index.html')
