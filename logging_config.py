import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    # Настройка логирования
    if not app.debug:
        # Убедимся, что директория для логов существует
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Создаем файловый обработчик
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'iko_api.log'),
            maxBytes=10485760,  # 10 МБ
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('IKO API запущен')