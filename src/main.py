import threading
import src.common.constants as c
from flask import Flask
from src.controller.customers_controller import customer_blueprint, timer_blueprint, telegram_blueprint
from src.infrastructure.telegram.telegram_app import bot_app

app = Flask(__name__)
app.register_blueprint(timer_blueprint)
app.register_blueprint(customer_blueprint)
app.register_blueprint(telegram_blueprint)


class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(host='0.0.0.0', port=c.PORT)


# class TelegramThread(threading.Thread):
#     def run(self) -> None:
#         app_run()


if __name__ == '__main__':
    # flask_thread = FlaskThread()
    # flask_thread.start()
    # app_run()
    WEBHOOK_URL = 'https://ms-tgbot-crab.onrender.com/telegram'
    # WEBHOOK_URL = 'http://localhost:5000/telegram'
    bot_app().bot.set_webhook(WEBHOOK_URL)

    app.run(host='0.0.0.0', port=c.PORT)
