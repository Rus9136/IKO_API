from flask import Flask, redirect
from flask_cors import CORS
from models.iko_document import db
from routes.iko_document_routes import bp as iko_bp
from api_docs import api_bp
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Разрешаем CORS для всех маршрутов
    CORS(app)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(iko_bp, url_prefix='/api/v1')
    app.register_blueprint(api_bp)

    # Redirect root to docs
    @app.route('/')
    def index():
        return redirect('/docs')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)