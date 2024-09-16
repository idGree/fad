# app/modules/team_set/models.py
"""
Модуль для определения модели данных TeamSet в приложении Flask.

Этот модуль содержит класс TeamSet, который представляет собой модель данных для хранения информации
о составе команд в базе данных. Модель используется для отображения связей между сотрудниками и командами,
а также их участия в проектах, измеряемого в единицах полной занятости (FTE).

Attributes:
    id (int): Уникальный идентификатор записи состава команды.
    team_id (int): Внешний ключ, указывающий на команду, к которой принадлежит данная запись.
    staff_id (int): Внешний ключ, указывающий на сотрудника, к которому принадлежит данная запись.
    fte (float): Значение FTE, указывающее участие сотрудника в команде (1.0 - полная занятость).

Определение отношений:
    team (relationship): Связь "многие к одному" с моделью Team, указывает на команду, к которой принадлежит состав.
    staff (relationship): Связь "многие к одному" с моделью Staff, указывает на сотрудника, входящего в состав команды.
"""
from app.db import db


class TeamSet(db.Model):
    __tablename__ = 'team_set'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    fte = db.Column(db.Float, nullable=False)

    # Обратные отношения, задающие связь "многие к одному" с Team и Staff.
    # back_populates указываем во множественном числе.
    # Эти отношения обеспечивают доступ к родительским записям Team и Staff для каждой записи TeamSet.
    # 'team' ссылается на одну команду (Team), к которой принадлежит данная запись TeamSet.
    # 'staff' ссылается на одного сотрудника (Staff), к которому принадлежит данная запись TeamSet.
    team = db.relationship('Team', back_populates='team_sets', lazy='select')
    staff = db.relationship('Staff', back_populates='team_sets', lazy='select')

    def __repr__(self):
        return f"<TeamSet(id={self.id}, team_id={self.team_id}, staff_id={self.staff_id}"
