import threading
from src.common.logger import log

from flask import Blueprint, jsonify, request
# from src.infrastructure.telegram.telegram_service import kick_all_inactive_customers
from src.infrastructure.telegram.telegram_app import bot_app
from src.service.customers_service import (
    get_customers,
    get_customer_by_client_uid,
    get_customer_by_uid,
    update_customer_trade_volumn,
    get_customer_trade_volumn_by_client_uid,
    volumn_calculator,
    get_all_customers_by_client,
    kick_member_by_uid,
    set_member_whitelist,
    get_customers_like_uid_admin,
    update_all_customers_trade_volumn,
    kick_group_members,
    update_customer_rejoin)

# bot = bot_app().bot

timer_blueprint = Blueprint('gettime', __name__, url_prefix='/api')
customer_blueprint = Blueprint('customer', __name__, url_prefix='/api')
telegram_blueprint = Blueprint('telegram', __name__, url_prefix='/api')


@timer_blueprint.route('/admin/gettime', methods=['GET'])
def get_all_customers():
    # test = get_customers()
    threading.Thread(target=bot_app()).start()
    return {'msg': "bot starting"}, 201


@customer_blueprint.route('/admin/customers', methods=['GET'])
def get_all_customers():
    customers = get_customers()
    return jsonify(customers)


@customer_blueprint.route('/admin/customer/<int:uid>', methods=['GET'])
def get_customer_by_uid_admin(uid):
    customer = get_customer_by_uid(uid)
    if customer:
        return jsonify(customer), 200
    else:
        return jsonify({'err': f"{uid} not found", 'status': 404}), 404
    # return jsonify(customer) if customer else jsonify({'err': f"{uid} not found", 'status': 404}), 404


@customer_blueprint.route('admin/customers/<int:uid>', methods=['GET'])
def get_customers_like_uid(uid):
    customers = get_customers_like_uid_admin(uid)
    return jsonify(customers), 200


@customer_blueprint.route('/customer/<int:uid>', methods=['GET'])
def get_customer_by_uid_from_client(uid):
    customer = get_customer_by_client_uid(uid)
    # customer = get_customer_by_uid(uid)
    if customer:
        return jsonify(customer)
    else:
        return jsonify({'err': f"{uid} not found", 'status': 404}), 404


@customer_blueprint.route('/admin/customer/whitelist', methods=["POST"])
def update_customer_whitelist():
    req = request.json
    uid = req.get('uid')
    log.info(req)
    is_whitelist = req.get('is_whitelist')
    customer = set_member_whitelist(uid, is_whitelist)
    if customer:
        return jsonify(customer)
    else:
        return jsonify({'err': f"{uid} not found", 'status': 404}), 404


@customer_blueprint.route('/admin/customer/delete', methods=['POST'])
def delete_customer():
    data = request.json
    uid = data.get('uid')
    # customer = get_customer_by_uid(uid)
    result = kick_member_by_uid(uid)
    if result:
        return jsonify(result), 201
    else:
        return jsonify({'err': "Bad Request", 'status': 400}), 400


@customer_blueprint.route('/customer/volumn/<int:uid>', methods=['GET'])
def get_customer_trade_volumn_by_uid(uid):
    # 8118815904
    customer = get_customer_trade_volumn_by_client_uid(uid)
    if customer:
        return jsonify(customer), 200
    else:
        return jsonify({'err': f"{uid} not found", 'status': 404}), 404


@customer_blueprint.route('/admin/customers/volumn/filter', methods=['POST'])
def update_all_customers_trade_volumn_by_date():
    req = request.json
    start_time = req.get('start_time')
    end_time = req.get('end_time')
    log.info("start_time=%s, end_time=%s", start_time, end_time)
    results = update_all_customers_trade_volumn(start_time, end_time)
    if results:
        return jsonify(results), 200
    else:
        return jsonify({'err': "Bad Request", 'status': 400}), 400


@customer_blueprint.route('/admin/customers/kickall', methods=['POST'])
def kick_all_customers_under_volumn_conditions():
    req = request.json
    volumn_condition = req.get('trade_volumn')
    result = kick_group_members(volumn_condition)
    return jsonify(result), 201


@customer_blueprint.route('/admin/customer/ban', methods=['POST'])
def update_member_ban_status():
    req = request.json
    uid = req.get('uid')
    is_ban = req.get('is_ban')
    result = update_customer_rejoin(uid, is_ban)
    return jsonify(result), 201

# @telegram_blueprint.route('/', methods=['POST'])
# def webhook():
#     log.info("running here1")
#     update = Update.de_json(request.json, bot_app().bot)
#     log.info("running here2")
#     bot_app().process_update(update)
#     log.info("running here3")
#     return 'OK', 200
