# app/modules/admin/user_views.py
"""
Настройки административной панели для управления пользователями.

Этот модуль содержит класс UserAdmin, который используется для настройки
административной панели Flask-Admin для модели пользователей. Класс
определяет отображение, редактирование и валидацию данных пользователей
в административной панели.
"""

from app.modules.admin.views import MyModelView
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_admin.form import Select2Widget
from werkzeug.security import generate_password_hash


class UserAdmin(MyModelView):
    """
    Класс для управления пользователями через Flask-Admin.
    """

    # Определяем, какие поля показывать в административной панели
    # list_template = 'admin/list.html'
    page_size = 100
    action_disallowed_list = ['delete', ]
    can_view_details = True  # show a modal dialog with records details

    column_list = ('id', 'user_name', 'user_email', 'role')
    column_searchable_list = ('user_name', 'user_email')
    column_sortable_list = ('id', 'user_name', 'user_email', 'role')
    form_columns = ('user_name', 'user_email', 'role')  # Пароль не указываем в модели
    column_labels = {
        'id': 'ID',
        'user_name': 'Имя пользователя',
        'user_email': 'Email',
        'role': 'Роль',
    }

    def create_form(self, obj=None):
        """
        Переопределяем метод создания формы для создания нового пользователя.
        """
        form = super(UserAdmin, self).create_form(obj)

        # Пример предустановки ролей
        form.role.choices = [('admin', 'Администратор'), ('user', 'Пользователь')]

        return form

    def edit_form(self, obj):
        """
        Переопределяем метод для редактирования формы пользователя.
        """
        form = super(UserAdmin, self).edit_form(obj)

        # Пример предустановки ролей
        form.role.choices = [('admin', 'Администратор'), ('user', 'Пользователь')]

        # Нет необходимости устанавливать form.role.data здесь, так как это автоматически устанавливается Flask-Admin

        return form

    def scaffold_form(self):
        """
        Создает форму для модели User с учетом дополнительных настроек.
        """
        form_class = super(UserAdmin, self).scaffold_form()

        # Поле для имени пользователя
        form_class.user_name = StringField('Имя пользователя', validators=[
            DataRequired(),
            Length(min=1, max=255)
        ])

        # Поле для Email
        form_class.user_email = StringField('Email', validators=[
            DataRequired(),
            Email(),
            Length(min=1, max=255)
        ])

        # Поле для выбора роли пользователя
        form_class.role = SelectField('Роль', widget=Select2Widget(), coerce=str)

        # Поля для ввода пароля и его подтверждения, но они не привязаны к модели напрямую
        form_class.password = PasswordField('Пароль', validators=[
            Length(min=3, max=16)
        ])

        form_class.confirm_password = PasswordField('Подтверждение пароля', validators=[
            EqualTo('password', message='Пароли должны совпадать')
        ])

        return form_class

    def on_model_change(self, form, model, is_created):
        """
        Переопределяем метод для хеширования пароля перед сохранением в базу и сохранения роли.
        """
        if form.password.data:
            # Если введен новый пароль, хешируем его и сохраняем
            model.password_hash = generate_password_hash(form.password.data)

        # Явно сохраняем роль пользователя
        if form.role.data:
            model.role = form.role.data

        return super(UserAdmin, self).on_model_change(form, model, is_created)

    def is_visible(self):
        # Скрываем из навигации
        return True