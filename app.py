from flask import Flask, redirect
from flask_cors import CORS
from models.iko_document import db
from routes.iko_document_routes import bp as iko_bp
from api_docs import api_bp
from config import Config
from sqlalchemy import inspect
from logging_config import configure_logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Настройка логирования
    configure_logging(app)
    
    # Разрешаем CORS для всех маршрутов
    CORS(app)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(iko_bp, url_prefix='/api/v1')
    app.register_blueprint(api_bp)
    
    # Импортируем health_bp
    try:
        from routes.health import health_bp
        app.register_blueprint(health_bp)
    except ImportError as e:
        app.logger.error(f"Не удалось импортировать health_bp: {e}")

    # Redirect root to docs
    @app.route('/')
    def index():
        return redirect('/docs')

    # Create database tables только если они не существуют
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('iko_documents'):
            app.logger.info("Создание таблиц базы данных")
            db.create_all()
        else:
            app.logger.info("Таблицы уже существуют, пропускаем создание")

    return app

# Создаем глобальную переменную app для Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
