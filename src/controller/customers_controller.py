from src.common.logger import log
from src.infrastructure.telegram.telegram_app import bot_app
from telegram import Update
from flask import Blueprint, jsonify, request

from src.service.customers_service import (
    get_customers,
    get_customer_by_client_uid,
    get_customer_by_uid,
    update_customer_trade_volumn,
    get_customer_trade_volumn_by_client_uid,
    volumn_calculator,
    get_all_customers_by_client)

bot = bot_app().bot

timer_blueprint = Blueprint('gettime', __name__, url_prefix='/gettime')
customer_blueprint = Blueprint('customer', __name__, url_prefix='/customer')
telegram_blueprint = Blueprint('telegram', __name__, url_prefix='/telegram')


@timer_blueprint.route('/', methods=['GET'])
def get_all_customers():
    server_time = get_customers()
    return jsonify(server_time)


@customer_blueprint.route('/<int:uid>', methods=['GET'])
def get_customer_by_id(uid):
    customer = get_customer_by_client_uid(uid)
    # customer = get_customer_by_uid(uid)
    if customer:
        return jsonify(customer)
    else:
        return jsonify({'err': f"{uid} not found", 'status': 404}), 404


@customer_blueprint.route('/volumn/<int:uid>', methods=['GET'])
def get_customer_trade_volumn_by_uid(uid):
    # 8118815904
    customer = get_customer_trade_volumn_by_client_uid(uid)
    if customer:
        return jsonify(customer)
    else:
        return jsonify({'err': f"{uid} not found", 'status': 404}), 404


@telegram_blueprint.route('/', methods=['POST'])
def webhook():
    log.info("running here1")
    update = Update.de_json(request.get_json(), bot)
    log.info("running here2")
    bot_app().process_update(update)
    log.info("running here3")
    return 'OK', 200
