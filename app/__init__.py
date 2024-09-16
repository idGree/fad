# app/__init__.py
"""
Инициализация основного Flask-приложения.

Этот модуль создает и конфигурирует экземпляр приложения Flask,
инициализирует расширения, такие как база данных, миграции и менеджер
сессий пользователей, а также регистрирует синие принты (blueprints)
для различных модулей приложения.
"""

# Третьесторонние библиотеки
from flask import Flask, render_template, redirect, url_for, request
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

# Локальные импорты
from app.db import db
from app.config.development import DevelopmentConfig
from utils.logging import configure_logging, log_and_flash

# Импортируем функцию для регистрации обработчиков ошибок
from app.modules.error.views import register_error_handlers

# Модели данных
from app.modules.user.models import User
from app.modules.staff.models import Staff
from app.modules.team.models import Team
from app.modules.team_set.models import TeamSet

# Вьюхи админки
from app.modules.admin.views import MyModelView, MyAdminIndexView
from app.modules.admin.user_views import UserAdmin
from app.modules.admin.staff_views import StaffAdmin
from app.modules.admin.team_views import TeamAdmin
from app.modules.admin.team_set_views import TeamSetAdmin

from app.modules.index.views import blueprint as index_bp
from app.modules.profile.views import blueprint as profile_bp
from app.modules.login.views import blueprint as login_bp
from app.modules.user.views import blueprint as user_bp
from app.modules.staff.views import blueprint as staff_bp
from app.modules.team.views import blueprint as team_bp
from app.modules.team_set.views import blueprint as team_set_bp
from app.modules.error.views import blueprint as error_bp

csrf = CSRFProtect()


def create_app(config_class=DevelopmentConfig):
    """
    Создает и конфигурирует экземпляр Flask-приложения.

    :param config_class: Класс конфигурации, который будет использоваться для настройки приложения.
    :type config_class: class

    :return: Настроенный экземпляр Flask-приложения.
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация CSRF-защиты
    csrf.init_app(app)

    # Инициализация расширений
    db.init_app(app)
    migrate = Migrate(app, db)

    # Настройка логирования
    configure_logging(app)

    # Настройка Flask-Login
    # Поскольку Flask-Login ничего не знает о базах данных, ему нужна помощь приложения при загрузке пользователя.
    # По этой причине расширение ожидает, что приложение настроит функцию загрузчика пользователя,
    # которую можно вызвать для загрузки пользователя с идентификатором.
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

    # Отключаем стандартное сообщение о доступе
    login_manager.login_message = None

    # login_manager.login_message = 'Доступ в личный кабинет разрешен только авторизованным пользователям!'
    # login_manager.login_message_category = 'danger'

    @login_manager.unauthorized_handler
    def handle_unauthorized():
        """
        Обрабатывает неавторизованные попытки доступа и выводит кастомное сообщение через log_and_flash.
        """
        log_and_flash('Доступ в личный кабинет разрешен только авторизованным пользователям!', 'danger')
        return redirect(url_for('login.login', next=request.url))

    # Настройка загрузчика пользователя для Flask-Login.
    @login_manager.user_loader
    def load_user(id):
        """
        Загружает пользователя по его идентификатору.

        Flask-Login использует эту функцию для получения данных о пользователе
        на основе его идентификатора.

        :param id: Идентификатор пользователя.
        :type id: int

        :return: Объект пользователя, если пользователь с таким идентификатором существует.
        :rtype: User or None
        """
        return User.query.get(id)

    # Регистрация blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(team_set_bp)
    app.register_blueprint(error_bp)

    # Регистрация обработчиков ошибок
    register_error_handlers(app)

    # Создание и регистрация Flask-Admin
    admin = Admin(app, name='Admin', template_mode='bootstrap4', base_template='admin/base.html', index_view=MyAdminIndexView())
    admin.add_view(UserAdmin(User, db.session, endpoint='users_admin', name='User'))
    admin.add_view(TeamAdmin(Team, db.session, endpoint='team_admin', name='Team'))
    admin.add_view(StaffAdmin(Staff, db.session, endpoint='staff_admin', name='Staff'))
    admin.add_view(TeamSetAdmin(TeamSet, db.session, endpoint='team_set_admin', name='TeamSet'))

    @app.route('/')
    def root():
        """
        Корневой маршрут приложения.

        :return: Редирект на главную страницу.
        :rtype: werkzeug.wrappers.Response
        """
        return redirect(url_for('index.index'))

    return app
