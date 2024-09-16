# app/modules/error/views.py
"""
Модуль с пользовательскими классами для ошибочных страниц.

Используется для организации и управления маршрутами (routes) и обработчиками запросов, связанными с этим модулем.
"""
from flask import Blueprint, render_template, request

# Создаем Blueprint для модуля error с префиксом '/error'
blueprint = Blueprint('error', __name__, url_prefix='/error')


def register_error_handlers(app):
    """
    Функция для регистрации обработчиков ошибок.

    :param app: Экземпляр Flask-приложения.
    :type app: Flask
    """

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Обработчик ошибки 404 - Not Found.
        Этот код ошибки возникает, когда пользователь запрашивает несуществующий маршрут.

        :param e: Ошибка 404.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 404.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 404: {request.url} не найдена')
        return render_template('member/errors.html', error_type=404, error_message="Page not found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """
        Обработчик ошибки 500 - Internal Server Error.
        Этот код ошибки указывает на проблемы на сервере, которые мешают обработке запроса.

        :param e: Ошибка 500.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 500.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 500: {request.url}')
        return render_template('member/errors.html', error_type=500, error_message="Internal server error"), 500

    @app.errorhandler(400)
    def bad_request_error(e):
        """
        Обработчик ошибки 400 - Bad Request.
        Этот код ошибки указывает на некорректный запрос от клиента.

        :param e: Ошибка 400.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 400.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 400: Некорректный запрос на {request.url}')
        return render_template('member/errors.html', error_type=400, error_message="Bad Request"), 400

    @app.errorhandler(401)
    def unauthorized_error(e):
        """
        Обработчик ошибки 401 - Unauthorized.
        Этот код ошибки указывает, что для доступа к ресурсу требуется авторизация.

        :param e: Ошибка 401.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 401.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 401: Неавторизованный доступ на {request.url}')
        return render_template('member/errors.html', error_type=401, error_message="Unauthorized"), 401

    @app.errorhandler(403)
    def forbidden_error(e):
        """
        Обработчик ошибки 403 - Forbidden.
        Этот код ошибки указывает, что доступ к запрашиваемому ресурсу запрещен.

        :param e: Ошибка 403.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 403.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 403: Доступ запрещен на {request.url}')
        return render_template('member/errors.html', error_type=403, error_message="Forbidden"), 403

    @app.errorhandler(405)
    def method_not_allowed_error(e):
        """
        Обработчик ошибки 405 - Method Not Allowed.
        Этот код ошибки указывает, что метод HTTP не поддерживается на данном ресурсе.

        :param e: Ошибка 405.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 405.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 405: Метод не разрешен на {request.url}')
        return render_template('member/errors.html', error_type=405, error_message="Method Not Allowed"), 405

    @app.errorhandler(409)
    def conflict_error(e):
        """
        Обработчик ошибки 409 - Conflict.
        Этот код ошибки указывает на конфликт запроса с текущим состоянием ресурса.

        :param e: Ошибка 409.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 409.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 409: Конфликт на {request.url}')
        return render_template('member/errors.html', error_type=409, error_message="Conflict"), 409

    @app.errorhandler(422)
    def unprocessable_entity_error(e):
        """
        Обработчик ошибки 422 - Unprocessable Entity.
        Этот код ошибки указывает, что сервер понимает запрос, но не может его обработать.

        :param e: Ошибка 422.
        :type e: Exception

        :return: Сгенерированный HTML-код страницы ошибки 422.
        :rtype: tuple (str, int)
        """
        app.logger.error(f'Ошибка 422: Необрабатываемый запрос на {request.url}')
        return render_template('member/errors.html', error_type=422, error_message="Unprocessable Entity"), 422
