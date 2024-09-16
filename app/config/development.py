# app/config/development.py
"""
Конфигурационный файл для режима разработки приложения Flask.

Этот модуль содержит глобальные настройки приложения для режима разработки,
включая параметры подключения к базе данных, параметры безопасности, а также различные
константы, используемые в приложении. В этом файле определяются такие параметры, как URI базы данных,
длительность cookies для сессии, ключ безопасности и настройки интерфейса Flask-Admin.
"""

import os
import logging
from datetime import timedelta


class DevelopmentConfig:
    """
    Конфигурация для режима разработки.

    Класс содержит настройки, специфичные для режима разработки, такие как
    URI базы данных, ключ безопасности и параметры cookies.

    :cvar BASEDIR: Базовая директория приложения.
    :cvar SQLALCHEMY_DATABASE_URI: URI для подключения к базе данных SQLite.
    :cvar SQLALCHEMY_TRACK_MODIFICATIONS: Флаг, указывающий, отслеживать ли изменения объектов SQLAlchemy.
    :cvar LOGIN_MESSAGE: Сообщение, которое выводится при неудачной попытке авторизации.
    :cvar REMEMBER_COOKIE_DURATION: Продолжительность жизни cookies для функции "Запомнить меня".
    :cvar SECRET_KEY: Секретный ключ для защиты сессий и CSRF.
    :cvar WTF_CSRF_ENABLED: Флаг, включающий защиту CSRF для форм.
    :cvar LOGS_DIR: Директория для хранения логов.
    :cvar LOG_FILE: Путь к файлу логов.
    :cvar LOGGING_LEVEL: Уровень логирования для приложения.
    """

    #: Базовая директория приложения
    BASEDIR = os.path.dirname(os.path.abspath(__file__))

    #: Директория для логов (находится на одном уровне с папкой app)
    LOGS_DIR = os.path.join(BASEDIR, '..', '..', 'logs')

    #: Путь к файлу логов
    LOG_FILE = os.path.join(LOGS_DIR, 'app.log')

    #: Уровень логирования
    LOGGING_LEVEL = logging.DEBUG

    #: URI базы данных для подключения к SQLite, используется для режима разработки
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, '..', 'app.db')

    #: Флаг для отключения отслеживания изменений объектов SQLAlchemy (экономит ресурсы памяти)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #: Сообщение, которое выводится при неудачной попытке авторизации
    LOGIN_MESSAGE = 'Ошибка! Вам доступ запрещен.'

    #: Длительность хранения cookies для функции "Запомнить меня"
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    #: Секретный ключ для защиты сессий и CSRF (загружается из .env)
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')

    #: Включение защиты CSRF для всех форм
    WTF_CSRF_ENABLED = True

    # Опциональные настройки для Flask-Admin
    # FLASK_ADMIN_SWATCH = 'default'
    # FLASK_ADMIN_FLUID_LAYOUT = True
