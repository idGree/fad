# app/modules/admin/staff_views.py

from datetime import datetime

from flask_admin.form import DatePickerWidget, DateTimePickerWidget
from wtforms import DateField, DateTimeField
from wtforms.validators import DataRequired

from app.modules.admin.views import MyModelView


class StaffAdmin(MyModelView):
    column_list = ['id', 'staff_name', 'staff_date', 'staff_datetime', 'staff_active', 'team_sets_count']
    column_searchable_list = ['staff_name']
    column_filters = ['staff_name', 'staff_date', 'staff_active']
    column_default_sort = ('id', True)
    form_excluded_columns = ['team_sets']

    def team_sets_count(self, obj):
        return len(obj.team_sets)

    column_formatters = {
        'team_sets_count': lambda view, context, model, name: view.team_sets_count(model),
        'staff_date': lambda v, c, m, p: m.staff_date.strftime('%d.%m.%Y') if m.staff_date else '',
        'staff_datetime': lambda v, c, m, p: m.staff_datetime.strftime('%d.%m.%Y %H:%M') if m.staff_datetime else '',
        'staff_active': lambda v, c, m, p: 'Да' if m.staff_active else 'Нет'
    }

    form_overrides = {
        'staff_date': DateField,
        'staff_datetime': DateTimeField
    }

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

    def create_form(self, obj=None):
        """Задаем значения по умолчанию только если они отсутствуют."""
        form = super(StaffAdmin, self).create_form(obj)

        # Если создаем новую запись, подставляем текущую дату и время только если они еще не заполнены
        if obj is None:
            if not form.staff_date.data:  # Проверяем, что поле даты пусто
                form.staff_date.data = datetime.utcnow().date()  # Текущая дата

            if not form.staff_datetime.data:  # Проверяем, что поле дата/время пусто
                form.staff_datetime.data = datetime.utcnow()  # Текущая дата и время

        return form

    def on_model_change(self, form, model, is_created):
        """Обрабатываем сохранение формы и записываем правильные данные в модель."""
        # Отладка для проверки значений формы
        print(f"staff_date: {form.staff_date.data}, staff_datetime: {form.staff_datetime.data}")

        # Если в форме есть данные для даты и времени, сохраняем их в модель
        if form.staff_date.data:
            model.staff_date = form.staff_date.data
        if form.staff_datetime.data:
            # Убедимся, что пользовательские данные перезаписывают значения по умолчанию
            model.staff_datetime = form.staff_datetime.data

        # Важно вызвать super для сохранения остальных полей
        return super(StaffAdmin, self).on_model_change(form, model, is_created)

    def __init__(self, model, session, **kwargs):
        super(StaffAdmin, self).__init__(model, session, **kwargs)
