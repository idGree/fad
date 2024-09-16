# app/modules/admin/team_views.py

"""
Этот файл отвечает за настройку административной панели Flask-Admin для управления командами (Team).
"""
from app.modules.admin.views import MyModelView


class TeamAdmin(MyModelView):
    # Позволяет отображать кнопку для просмотра подробностей записи.
    # При установке значения True, рядом с каждой записью в списке появится иконка для просмотра.
    can_view_details = True

    #: Список колонок, отображаемых в административной панели
    column_list = ['id', 'team_name', 'team_sets_count']

    #: Колонки, по которым можно производить поиск
    column_searchable_list = ['team_name']

    #: Сортировка по умолчанию (по ID в порядке возрастания)
    column_default_sort = ('id', True)

    #: Колонки, по которым можно сортировать
    column_sortable_list = ['id', 'team_name']

    column_formatters = {
        'team_sets_count': lambda view, context, model, name: view.team_sets_count(model)
    }

    #: Переопределение названий колонок для удобства пользователя
    column_labels = {
        'id': 'ID',
        'team_name': 'Название команды',
        'team_sets_count': 'BD Links'
    }

    @staticmethod
    def team_sets_count(obj):
        """
        Возвращает количество наборов команды для указанного объекта команды.

        :param obj: Экземпляр модели команды.
        :return: Количество наборов команды.
        :rtype: int
        """

        return len(obj.team_sets)

    def __init__(self, model, session, **kwargs):
        super(TeamAdmin, self).__init__(model, session, **kwargs)
