# app/modules/team/models.py
"""
Модуль для определения модели данных Team в приложении Flask.

Этот модуль содержит класс Team, который представляет собой модель данных для хранения информации
о командах в базе данных. Модель используется для управления командами в проекте и связи
с составами команд, определенными в модели TeamSet.

Attributes:
    id (int): Уникальный идентификатор команды.
    team_name (str): Название команды.

Определение отношений:
    team_sets (relationship): Связь "один ко многим" с моделью TeamSet. Определяет все записи TeamSet,
                              связанные с данной командой. Это отношение позволяет легко получить доступ
                              ко всем составам команды.
"""
from app.db import db


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String, nullable=False)

    # Отношение "один ко многим" между Team и TeamSet.
    # back_populates указываем в единственном числе.
    # Это отношение позволяет получить доступ ко всем записям TeamSet, связанным с данной командой (Team).
    team_sets = db.relationship('TeamSet', back_populates='team', lazy='select')

    def __repr__(self):
        return f"<Team(id={self.id}, team_name={self.team_name})>"
