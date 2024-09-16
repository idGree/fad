# app/modules/admin/team_set_views.py
"""
Модуль team_set_views.py отвечает за настройку административной панели Flask-Admin для управления наборами команд (TeamSet).

Основные функции:
1. Отображение и управление записями TeamSet в административной панели.
2. Обеспечение поиска, сортировки и фильтрации данных по ключевым полям (команда, сотрудник, процент утилизации).
3. Поддержка удобных виджетов выбора (Select2) для полей команды и сотрудника.
4. Форматирование отображаемых данных, таких как имена команд и сотрудников, для лучшего представления.
5. Обработка создания и редактирования записей TeamSet через административную панель.

Основные классы:
- TeamSetForm: Форма для создания и редактирования набора команды (TeamSet).
- TeamSetAdmin: Административное представление модели TeamSet, включая настройку отображения колонок, фильтров, сортировки и виджетов для удобного ввода данных.
"""

from flask_admin.form import Select2Widget
from wtforms import FloatField, SelectField, Form
from wtforms.validators import DataRequired

from app.modules.admin.views import MyModelView
from app.modules.staff.models import Staff
from app.modules.team.models import Team


class TeamSetForm(Form):
    """
    Форма для создания и редактирования набора команд (TeamSet) в административной панели.

    Поля формы:
    - team_id: Выбор команды из связанных записей модели Team.
    - staff_id: Выбор сотрудника из связанных записей модели Staff.
    - fte: Процент времени (FTE), который сотрудник тратит на работу в команде.
    """
    team_id = SelectField('Team', widget=Select2Widget(), coerce=int, validators=[DataRequired()])
    staff_id = SelectField('Staff', widget=Select2Widget(), coerce=int, validators=[DataRequired()])
    fte = FloatField('FTE')


class TeamSetAdmin(MyModelView):
    """
    Класс для управления набором команд (TeamSet) в административной панели Flask-Admin.

    Этот класс предоставляет интерфейс для управления записями TeamSet, включая отображение,
    сортировку, фильтрацию и редактирование данных через административную панель.

    :param model: Модель SQLAlchemy, представляющая набор команды (TeamSet).
    :param session: Сессия SQLAlchemy для выполнения операций с базой данных.
    """

    # Позволяет отображать кнопку для просмотра подробностей записи.
    # При установке значения True, рядом с каждой записью в списке появится иконка для просмотра.
    can_view_details = True

    #: Список колонок, отображаемых в административной панели
    column_list = ['id', 'team_name', 'staff_name', 'fte']

    #: Колонки, по которым можно производить поиск
    column_searchable_list = ['team.team_name', 'staff.staff_name']

    #: Сортировка по умолчанию (по ID в порядке возрастания)
    column_default_sort = ('team_id', True)

    #: Колонки, по которым можно сортировать
    column_sortable_list = [
        'id',
        ('team_name', 'team.team_name'),  # Сортировка по связанной модели Team
        ('staff_name', 'staff.staff_name'),  # Сортировка по связанной модели Staff
        'fte'
    ]

    #: Переопределение названий колонок для удобства пользователя
    column_labels = {
        'id': 'ID',
        'team_name': 'Команда',
        'team.team_name': 'Поиск (team)',
        'staff_name': 'Сотрудник',
        'staff.staff_name': 'Поиск (staff)',
        'fte': '% утилизации'
    }

    # form_excluded_columns = []

    form = TeamSetForm

    def __init__(self, model, session, **kwargs):
        """
        Инициализирует административную панель для модели TeamSet.

        :param model: Модель SQLAlchemy, представляющая набор команды (TeamSet).
        :param session: Сессия SQLAlchemy для выполнения операций с базой данных.
        :param kwargs: Дополнительные параметры.
        """

        super(TeamSetAdmin, self).__init__(model, session, **kwargs)

    def _populate_choices(self, form):
        """
        Заполняет список доступных вариантов для полей выбора команды и сотрудника.

        :param form: Форма, в которой необходимо обновить варианты выбора.
        :return: Обновленная форма с заполненными списками вариантов для полей team_id и staff_id.
        """

        form.team_id.choices = [(0, 'Select a team')] + [(team.id, team.team_name) for team in self.session.query(Team).all()]
        form.staff_id.choices = [(0, 'Select a staff')] + [(staff.id, staff.staff_name) for staff in self.session.query(Staff).all()]
        return form

    def create_form(self, obj=None):
        """
        Создает форму для добавления записи TeamSet в административной панели.

        :param obj: Экземпляр модели TeamSet, если редактируется существующая запись, иначе None.
        :return: Форма для создания новой записи TeamSet с заполненными вариантами выбора.
        """

        form = super(TeamSetAdmin, self).create_form(obj)
        return self._populate_choices(form)

    def edit_form(self, obj=None):
        """
        Создает форму для редактирования существующей записи TeamSet в административной панели.

        :param obj: Экземпляр модели TeamSet, который необходимо отредактировать.
        :return: Форма для редактирования записи TeamSet с заполненными вариантами выбора.
        """

        form = super(TeamSetAdmin, self).edit_form(obj)
        return self._populate_choices(form)

    @staticmethod
    def _team_name_formatter(view, context, model, name):
        """
        Форматирует отображение имени команды в административной панели.

        :param view: Представление административной панели.
        :param context: Контекст, в котором отображается колонка.
        :param model: Экземпляр модели TeamSet.
        :param name: Имя поля, которое необходимо отформатировать.
        :return: Строка с названием команды.
        """

        return model.team.team_name

    @staticmethod
    def _staff_name_formatter(view, context, model, name):
        """
        Форматирует отображение имени сотрудника в административной панели.

        :param view: Представление административной панели.
        :param context: Контекст, в котором отображается колонка.
        :param model: Экземпляр модели TeamSet.
        :param name: Имя поля, которое необходимо отформатировать.
        :return: Строка с именем сотрудника.
        """

        return model.staff.staff_name

    #: Форматирование в колонках
    column_formatters = {
        'team_name': _team_name_formatter,
        'staff_name': _staff_name_formatter
    }
