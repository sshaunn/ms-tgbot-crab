import threading
import time

from flask import Flask
from flask_cors import CORS

from src.common.logger import log
from src.controller.admin_controller import admin_blueprint
from src.controller.customers_controller import customer_blueprint, timer_blueprint, telegram_blueprint
from src.infrastructure.telegram.telegram_app import bot_app

app = Flask(__name__)
CORS(app)
app.register_blueprint(timer_blueprint)
app.register_blueprint(customer_blueprint)
app.register_blueprint(telegram_blueprint)
app.register_blueprint(admin_blueprint)


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()
    while True:
        try:
            bot_app()
        except Exception as e:
            log.info("Telegram bot crashed with exception=%s, restarting...", e)
            time.sleep(5)
