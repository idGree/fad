# app/modules/admin/staff_views.py
"""
Модуль staff_views.py отвечает за настройку отображения и обработки данных сотрудников
в административной панели приложения с использованием Flask-Admin.

Основные задачи:
1. Отображение списка сотрудников с возможностью фильтрации, сортировки и поиска.
2. Форматирование отображаемых данных, включая использование виджетов для ввода дат и времени.
3. Обработка создания и редактирования записей сотрудников с автоматическим добавлением текущей даты и времени.
"""
from datetime import datetime

from flask_admin.form import DatePickerWidget, DateTimePickerWidget
from wtforms import DateField, DateTimeField
from wtforms.validators import DataRequired

from app.modules.admin.views import MyModelView


class StaffAdmin(MyModelView):
    """
    Класс StaffAdmin отвечает за управление моделью сотрудников (Staff) в административной панели Flask-Admin.

    Этот класс позволяет:
    - Отображать и форматировать список сотрудников.
    - Поддерживать фильтрацию, сортировку и поиск по полям.
    - Обрабатывать формы для создания и редактирования сотрудников с автоматической подстановкой текущей даты и времени.

    :param model: Модель SQLAlchemy, представляющая сущность сотрудника.
    :param session: Сессия SQLAlchemy для взаимодействия с базой данных.
    """

    # Позволяет отображать кнопку для просмотра подробностей записи.
    # При установке значения True, рядом с каждой записью в списке появится иконка для просмотра.
    can_view_details = True

    #: Список колонок, отображаемых в административной панели
    column_list = ['id', 'staff_name', 'staff_date', 'staff_datetime', 'staff_active', 'team_sets_count']

    #: Колонки, по которым можно производить поиск
    column_searchable_list = ['staff_name']

    #: Сортировка по умолчанию (по ID в порядке возрастания)
    column_default_sort = ('id', True)

    #: Колонки, по которым можно сортировать
    column_sortable_list = ['id', 'staff_name', 'staff_date', 'staff_datetime', 'staff_active']

    #: Форматирование в колонках административной панели
    column_formatters = {
        'team_sets_count': lambda view, context, model, name: view.team_sets_count(model),
        'staff_date': lambda v, c, m, p: m.staff_date.strftime('%d.%m.%Y') if m.staff_date else '',
        'staff_datetime': lambda v, c, m, p: m.staff_datetime.strftime('%d.%m.%Y %H:%M') if m.staff_datetime else '',
        'staff_active': lambda v, c, m, p: 'Да' if m.staff_active else 'Нет'
    }

    #: Переопределение полей формы для ввода дат и времени
    form_overrides = {
        'staff_date': DateField,
        'staff_datetime': DateTimeField
    }

    #: Аргументы для настройки полей формы
    form_args = {
        'staff_date': {
            'label': 'Дата',
            'widget': DatePickerWidget(),
            'format': '%Y-%m-%d',  # Убедитесь, что формат соответствует ожиданиям HTML5
            'validators': [DataRequired()],
            'render_kw': {'type': 'date', 'class': 'form-control'}  # Указываем класс для стилей
        },
        'staff_datetime': {
            'label': 'Дата и время',
            'widget': DateTimePickerWidget(),
            'format': '%Y-%m-%dT%H:%M',  # Проверьте, что формат соответствует тому, что поддерживается input datetime-local
            'validators': [DataRequired()],
            'render_kw': {'type': 'datetime-local', 'class': 'form-control'}
        }
    }

    #: Переопределение названий колонок для удобства пользователя
    column_labels = {
        'id': 'ID',
        'staff_name': 'Имя сотрудника',
        'staff_date': 'Дата',
        'staff_datetime': 'Дата&Время',
        'staff_active': 'Активный?',
        'team_sets_count': 'BD Links'
    }

    def __init__(self, model, session, **kwargs):
        """
        Инициализация административной панели для модели сотрудника.

        :param model: Модель SQLAlchemy, представляющая сущность сотрудника.
        :param session: Сессия SQLAlchemy для взаимодействия с базой данных.
        :param kwargs: Дополнительные параметры.
        """
        super(StaffAdmin, self).__init__(model, session, **kwargs)

    @staticmethod
    def team_sets_count(obj):
        """
        Возвращает количество наборов команды для сотрудника.

        :param obj: Экземпляр модели сотрудника.
        :return: Количество наборов команды у сотрудника.
        :rtype: int
        """
        return len(obj.team_sets)

    def create_form(self, obj=None):
        """
        Создает форму для добавления или редактирования сотрудника.

        Если создается новая запись, текущие дата и время будут подставлены
        в соответствующие поля.

        :param obj: Экземпляр модели, если редактируется существующая запись, иначе None.
        :return: Форма для создания или редактирования записи.
        :rtype: wtforms.Form
        """
        # Задаем значения по умолчанию только если они отсутствуют.
        form = super(StaffAdmin, self).create_form(obj)

        # Если создаем новую запись, подставляем текущую дату и время только если они еще не заполнены
        if obj is None:
            if not form.staff_date.data:  # Проверяем, что поле даты пусто
                form.staff_date.data = datetime.utcnow().date()  # Текущая дата

            if not form.staff_datetime.data:  # Проверяем, что поле дата/время пусто
                form.staff_datetime.data = datetime.utcnow()  # Текущая дата и время

        return form

    def on_model_change(self, form, model, is_created):
        """
        Обрабатывает изменения модели при создании или редактировании сотрудника.

        Обновляет значения полей даты и времени в модели на основе введенных данных.

        :param form: Форма с данными, введенными пользователем.
        :param model: Модель сотрудника, в которую записываются данные.
        :param is_created: Флаг, указывающий, создается новая запись или редактируется существующая.
        :return: Измененная модель с обновленными данными.
        :rtype: SQLAlchemy модель
        """

        # Отладка для проверки значений формы
        # print(f"staff_date: {form.staff_date.data}, staff_datetime: {form.staff_datetime.data}")

        # Если в форме есть данные для даты и времени, сохраняем их в модель
        if form.staff_date.data:
            model.staff_date = form.staff_date.data
        if form.staff_datetime.data:
            # Убедимся, что пользовательские данные перезаписывают значения по умолчанию
            model.staff_datetime = form.staff_datetime.data

        # Важно вызвать super для сохранения остальных полей
        return super(StaffAdmin, self).on_model_change(form, model, is_created)


