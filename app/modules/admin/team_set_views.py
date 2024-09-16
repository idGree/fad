# app/modules/admin/team_set_views.py

from flask_admin.form import Select2Widget
from wtforms import FloatField, SelectField, Form
from wtforms.validators import DataRequired

from app.modules.admin.views import MyModelView
from app.modules.staff.models import Staff
from app.modules.team.models import Team


class TeamSetForm(Form):
    team_id = SelectField('Team', widget=Select2Widget(), coerce=int, validators=[DataRequired()])
    staff_id = SelectField('Staff', widget=Select2Widget(), coerce=int, validators=[DataRequired()])
    fte = FloatField('FTE')


class TeamSetAdmin(MyModelView):
    #: Список колонок, отображаемых в административной панели
    column_list = ['id', 'team_name', 'staff_name', 'fte']

    #: Колонки, по которым можно производить поиск
    column_searchable_list = ['team.team_name', 'staff.staff_name']

    column_default_sort = ('team_id', True)

    #: Переопределение названий колонок для удобства пользователя
    column_labels = {
        'id': 'ID',
        'team_name': 'Команда',
        'staff_name': 'Сотрудник',
        'fte': '% утилизации'
    }

    #: Колонки, по которым можно сортировать
    column_sortable_list = [
        'id',
        ('team_name', 'team.team_name'),  # Сортировка по связанной модели Team
        ('staff_name', 'staff.staff_name'),  # Сортировка по связанной модели Staff
        'fte'
    ]


    form_excluded_columns = []

    form = TeamSetForm

    def __init__(self, model, session, **kwargs):
        super(TeamSetAdmin, self).__init__(model, session, **kwargs)

    def _populate_choices(self, form):
        form.team_id.choices = [(0, 'Select a team')] + [(team.id, team.team_name) for team in self.session.query(Team).all()]
        form.staff_id.choices = [(0, 'Select a staff')] + [(staff.id, staff.staff_name) for staff in self.session.query(Staff).all()]
        return form

    def create_form(self, obj=None):
        form = super(TeamSetAdmin, self).create_form(obj)
        return self._populate_choices(form)

    def edit_form(self, obj=None):
        form = super(TeamSetAdmin, self).edit_form(obj)
        return self._populate_choices(form)

    def _team_name_formatter(view, context, model, name):
        return model.team.team_name

    def _staff_name_formatter(view, context, model, name):
        return model.staff.staff_name

    #: Форматирование в колонках
    column_formatters = {
        'team_name': _team_name_formatter,
        'staff_name': _staff_name_formatter
    }
