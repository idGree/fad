# app/utils/app_logging.py
"""
Модуль для настройки логирования в приложении Flask.

Этот модуль предоставляет функции и классы для настройки и форматирования логирования,
включая добавление пользовательских данных в логи, таких, как email пользователя и его IP-адрес.
Логирование выполняется как в файл, так и в консоль с возможностью цветного форматирования для консоли.
Логи включают детальную информацию о месте возникновения события, что облегчает отладку и мониторинг
приложения в процессе эксплуатации.
"""
import logging
import os

from flask import current_app, request, flash
from flask_login import current_user
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter




class RequestUserFilter(logging.Filter):
    """
    Класс для добавления информации о пользователе и IP-адресе в каждый лог.

    Этот фильтр добавляет в записи логов информацию о текущем пользователе и его IP-адресе.

    Методы:
        filter(record): Добавляет email пользователя и IP-адрес к записи лога.

    :param record.user: Email пользователя, если он авторизован, иначе 'ANONYMOUS' или 'UNKNOWN'.
    :type record.user: str
    :param record.ip: IP-адрес пользователя, если он доступен, иначе 'UNKNOWN IP'.
    :type record.ip: str
    """

    def filter(self, record):
        try:
            # Проверяем, авторизован ли пользователь
            if current_user.is_authenticated:
                record.user = current_user.user_email  # Используем user_email вместо user_name
            else:
                record.user = 'ANONYMOUS'
        except Exception:
            record.user = 'UNKNOWN'

        try:
            # Получаем IP-адрес пользователя
            record.ip = request.remote_addr if request else 'UNKNOWN IP'
        except Exception:
            record.ip = 'UNKNOWN IP'

        return True


def configure_logging(app):
    """
    Настраивает логирование для приложения Flask.

    Эта функция настраивает логирование как в файл, так и в консоль. В каждом логе записываются
    информация о пользователе и его IP-адресе. Логи в консоли выводятся с цветным форматированием
    для улучшения визуального восприятия.

    :param app: Приложение Flask, для которого настраивается логирование.
    :type app: Flask
    """
    # Создаем директорию для логов, если она не существует
    if not os.path.exists(app.config['LOGS_DIR']):
        os.makedirs(app.config['LOGS_DIR'])

    # Создаем фильтр для добавления email и IP пользователя
    user_filter = RequestUserFilter()

    # Настройка логирования в файл
    file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10240, backupCount=10)
    file_handler.setLevel(app.config['LOGGING_LEVEL'])
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: [%(user)s] [%(ip)s] %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(user_filter)
    app.logger.addHandler(file_handler)

    # Настройка логирования в консоль с цветами
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s: [%(user)s] [%(ip)s] %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(user_filter)
    app.logger.addHandler(console_handler)

    # Устанавливаем уровень логирования для логгера приложения
    app.logger.setLevel(logging.DEBUG)

    app.logger.info('Flask приложение запущено')


def log_and_flash(message, category='info'):
    """
    Универсальная функция для логирования и вывода flash-сообщений.

    Эта функция позволяет одновременно выводить flash-сообщения для пользователя и логировать их
    с указанием уровня логирования, соответствующего категории сообщения.

    :param message: Текст сообщения, которое нужно вывести пользователю и записать в лог.
    :type message: str
    :param category: Категория сообщения (info, warning, error, critical и т.д.).
    :type category: str
    """
    # Отправляем flash-сообщение пользователю
    flash(message, category)

    # Логируем сообщение в зависимости от категории
    logger = current_app.logger
    if category == 'info':
        logger.info(message)
    elif category == 'warning':
        logger.warning(message)
    elif category == 'danger':
        logger.error(message)
    elif category == 'critical':
        logger.critical(message)
    else:
        logger.debug(message)
