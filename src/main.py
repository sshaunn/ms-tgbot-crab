import threading
from flask import Flask
from src.controller.customers_controller import customer_blueprint, timer_blueprint, telegram_blueprint
from src.infrastructure.telegram.telegram_app import app_run

app = Flask(__name__)
app.register_blueprint(timer_blueprint)
app.register_blueprint(customer_blueprint)
app.register_blueprint(telegram_blueprint)


class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(port=8080)


class TelegramThread(threading.Thread):
    def run(self) -> None:
        app_run()


if __name__ == '__main__':
    # flask_thread = FlaskThread()
    # flask_thread.start()
    # app_run()

    app.run(port=8080)
