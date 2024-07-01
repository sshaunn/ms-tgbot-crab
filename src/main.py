import threading
import src.common.constants as c
from flask import Flask, render_template
from flask_cors import CORS
from src.controller.customers_controller import customer_blueprint, timer_blueprint, telegram_blueprint
from src.infrastructure.telegram.telegram_app import bot_app

app = Flask(__name__)
CORS(app)
app.register_blueprint(timer_blueprint)
app.register_blueprint(customer_blueprint)
app.register_blueprint(telegram_blueprint)


class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(host='0.0.0.0', port=c.PORT)


class TelegramThread(threading.Thread):
    def run(self) -> None:
        bot_app()


if __name__ == '__main__':
    # flask_thread = FlaskThread()
    # flask_thread.start()
    # bot_app()
    # threading.Thread(target=bot_app()).start()
    app.run(host='0.0.0.0', port=c.PORT)
