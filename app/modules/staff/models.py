# app/modules/staff/models.py
"""
Модуль для определения модели данных Staff в приложении Flask.

Этот модуль содержит класс Staff, который представляет собой модель данных для хранения информации
о сотрудниках в базе данных. Модель используется для управления сотрудниками в проекте и связи
с составами команд, определенными в модели TeamSet.

Attributes:
    id (int): Уникальный идентификатор сотрудника.
    staff_name (str): Имя сотрудника.
    staff_date (Date): Дата, связанная с сотрудником (например, дата начала работы).
    staff_datetime (DateTime): Дата и время, связанные с сотрудником (например, время последнего входа).
    staff_active (bool): Статус активности сотрудника - еще работает или уже нет.

Определение отношений:
    team_sets (relationship): Связь "один ко многим" с моделью TeamSet. Определяет все записи TeamSet,
                              связанные с данным сотрудником. Это отношение позволяет легко получить доступ
                              ко всем командам, в которых участвует сотрудник.
"""
from app.db import db


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String, nullable=False)
    staff_date = db.Column(db.Date, nullable=False)
    staff_datetime = db.Column(db.DateTime)
    staff_active = db.Column(db.Boolean, nullable=False)

    # Отношение "один ко многим" между Staff и TeamSet.
    # back_populates указываем в единственном числе.
    # Это отношение позволяет получить доступ ко всем записям TeamSet, связанным с данным сотрудником (Staff).
    team_sets = db.relationship('TeamSet', back_populates='staff', lazy='select')

    def __repr__(self):
        return f"<Staff(id={self.id}, staff_name={self.staff_name})>"
