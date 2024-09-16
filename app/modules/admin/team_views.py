# app/modules/admin/team_views.py

"""
Этот файл отвечает за настройку административной панели Flask-Admin для управления командами (Team).
"""
from app.modules.admin.views import MyModelView


class TeamAdmin(MyModelView):
    column_list = ['id', 'team_name', 'team_sets_count']
    column_searchable_list = ['team_name']
    column_filters = ['team_name']
    column_default_sort = ('team_name', True)
    form_excluded_columns = ['team_sets']
    column_default_sort = ('id', True)

    def team_sets_count(self, obj):
        return len(obj.team_sets)

    column_formatters = {
        'team_sets_count': lambda view, context, model, name: view.team_sets_count(model)
    }

    def __init__(self, model, session, **kwargs):
        super(TeamAdmin, self).__init__(model, session, **kwargs)
