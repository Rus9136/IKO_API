from flask import Flask, redirect
from flask_cors import CORS
from models.iko_document import db
from config import Config
from sqlalchemy import inspect
from logging_config import configure_logging
from flask_migrate import Migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Настройка логирования
    configure_logging(app)
    
    # Разрешаем CORS для всех маршрутов
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Импортируем и регистрируем маршруты
    from routes.iko_document_routes import document_bp
    from routes.iko_check_routes import check_bp
    from routes.health import health_bp
    from api_docs import api_bp

    # Register blueprints
    app.register_blueprint(document_bp, url_prefix='/api')
    app.register_blueprint(check_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(api_bp)

    # Redirect root to docs
    @app.route('/')
    def index():
        return redirect('/docs')

    # Create database tables только если они не существуют
    try:
        # Проверим, используется ли SQLite или PostgreSQL
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        if 'sqlite' in db_url:
            app.logger.info(f"Используется SQLite: {db_url}")
        else:
            app.logger.info(f"Используется PostgreSQL: {db_url}")
            
        with app.app_context():
            inspector = inspect(db.engine)
            if not inspector.has_table('sales_receipts'):
                app.logger.info("Создание таблиц базы данных")
                db.create_all()
            else:
                app.logger.info("Таблицы уже существуют, пропускаем создание")
    except Exception as e:
        app.logger.error(f"Ошибка подключения к базе данных: {str(e)}")
        app.logger.warning("Запуск приложения без подключения к базе данных. Функциональность будет ограничена.")
    
    # Вывод всех зарегистрированных маршрутов для отладки
    app.logger.info("Зарегистрированные маршруты:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda x: str(x)):
        app.logger.info(f"Route: {rule.rule} -> {rule.endpoint}")

    return app

# Создаем глобальную переменную app для Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
