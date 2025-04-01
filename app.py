from flask import Flask
from flask_cors import CORS
from models.iko_document import db
from routes.iko_document_routes import bp as iko_bp
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app)
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(iko_bp, url_prefix='/api/v1')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)