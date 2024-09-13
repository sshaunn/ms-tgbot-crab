import time
import datetime as dt
import src.repository.customers_repository_helper as customer_helper
import requests

import src.common.constants as c
from datetime import datetime
from src.common.logger import log
from src.bitget import utils
from src.bitget.bitget_api import BitgetApi as baseApi


def get_customers_with_pagination(limit, offset):
    return customer_helper.get_customers_with_pagination(limit, offset * limit)


def get_customers_count():
    return customer_helper.get_customers_count()


def delete_customer_from_db(uid):
    return customer_helper.delete_customer(uid)


def get_customers():
    # url = f"{c.BASE_URL}{c.SERVER_TIME_ENDPOINT}"
    # response = requests.get(url)
    customers = customer_helper.get_all_customers()
    list(map(lambda x: {'register_time': x['register_time'] if x['register_time'] else None,
                        'join_time': x['join_time'] if x['join_time'] else None,
                        'left_time': x['left_time'] if x['left_time'] else None}, customers))
    # customer_helper.save_customer(101, "shaun", "shen", "101", "1710845728000")
    return customers


def get_customer_by_client_uid(uid):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    params = {"uid": uid,
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.AGENT_ENDPOINT, params)
    time.sleep(0.1)
    if not response["data"]:
        return None
    log.info("checking customer success with uid=%s, user=%s", uid, response['data'][0])
    return response["data"][0]


def get_all_customers_by_client():
    """fucking stupid BITGET API, can only get 120 records, WTF is this shit.... ffs"""
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    today = datetime.now()
    last_month = today.replace(day=1) - dt.timedelta(days=24 * 30)
    epoch_ms = int(last_month.timestamp() * 1000)
    params = {"startTime": str(epoch_ms),
              "endTime": str(utils.get_timestamp()),
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.AGENT_ENDPOINT, params)
    time.sleep(0.1)
    if not response:
        return None
    return {"length": len(response['data']), "details": response['data']}


def get_customer_trade_volumn_by_client_uid(uid):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    today = datetime.now()
    last_month = today.replace(day=1) - dt.timedelta(days=30)
    epoch_ms = int(last_month.timestamp() * 1000)
    params = {"uid": uid,
              "startTime": str(epoch_ms),
              "endTime": str(utils.get_timestamp()),
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.VOLUMN_ENDPOINT, params)
    time.sleep(0.1)
    if not response["data"]:
        return None
    return response['data']


def volumn_calculator(uid):
    total_volumn = 0
    trades = get_customer_trade_volumn_by_client_uid(uid)
    for trade in trades:
        total_volumn += float(trade['volumn'])
    return round(total_volumn, 2)


def get_customer_by_uid(uid):
    customer = customer_helper.get_customer_by_uid(uid)
    return customer


def get_customers_like_uid_admin(uid):
    customers = customer_helper.get_customer_like_uid(uid)
    return customers


def get_customer_by_key(keyname, value):
    customer = customer_helper.get_customer_by_key(keyname, value)
    return customer


def get_customer_ban_status_by_uid(uid):
    customer = customer_helper.get_customer_ban_status_by_uid(uid)
    return customer


def save_customer(uid, firstname, lastname, tgid, register_time, is_member=False, is_whitelist=False, is_ban=False,
                  join_time=None, left_time=None):
    customer = customer_helper.save_customer(uid, firstname, lastname, tgid, register_time, is_member, is_whitelist,
                                             is_ban, join_time, left_time)
    return customer


def update_customer_trade_volumn_by_client(uid):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    today = datetime.now()
    last_month = today.replace(day=1) - dt.timedelta(days=30)
    epoch_ms = int(last_month.timestamp() * 1000)
    params = {"uid": uid,
              "startTime": str(epoch_ms),
              "endTime": str(utils.get_timestamp()),
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.VOLUMN_ENDPOINT, params)
    time.sleep(0.11)
    trade_list = response["data"] if response["data"] else None
    if not trade_list:
        return None
    total_volumn = utils.volumn_calculator(trade_list)
    customer = customer_helper.update_customer_volumn(uid, total_volumn)
    return customer


def update_customer_trade_volumn(uid, start_time, end_time):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    # today = datetime.now()
    # last_month = today.replace(day=1) - dt.timedelta(days=1)
    # epoch_ms = int(last_month.timestamp() * 1000)
    params = {"uid": uid,
              "startTime": start_time,
              "endTime": end_time,
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.VOLUMN_ENDPOINT, params)
    time.sleep(0.11)
    trade_list = response["data"] if response["data"] else None
    if not trade_list:
        return None
    total_volumn = utils.volumn_calculator(trade_list)
    log.info("total_volumn=%s", total_volumn)
    customer = customer_helper.update_customer_volumn(uid, total_volumn)
    return customer


def update_all_customers_trade_volumn(start_time, end_time):
    customers = get_customers()
    for customer in customers:
        update_customer_trade_volumn(customer['uid'], start_time, end_time)
    return customers


def update_customer_membership(uid, membership):
    customer = customer_helper.update_customer_membership(uid, membership)
    return customer


def update_customer_ban_status(uid, is_member, is_ban, left_time):
    customer = customer_helper.update_customer_ban_status(uid, is_member, is_ban, left_time)
    return customer


def update_customer_rejoin(uid, is_ban):
    customer = customer_helper.update_customer_rejoin(uid, is_ban)
    return customer


def kick_member_by_uid(uid):
    url_kick = f"{c.TELEGRAM_API_PREFIX}/kickChatMember"
    url_unban = f"{c.TELEGRAM_API_PREFIX}/unbanChatMember"
    customer = customer_helper.get_customer_by_uid(uid)
    if not customer['is_whitelist']:
        params_kick = {
            "chat_id": c.VIP_GROUP_ID,
            "user_id": customer['tgid'],
            "until_date": int(time.time())
        }
        params_unban = {
            "chat_id": c.VIP_GROUP_ID,
            "user_id": customer['tgid'],
        }
        requests.post(url_kick, params=params_kick)
        requests.post(url_unban, params=params_unban)
        customer_helper.update_customer_ban_status(customer['uid'], False, True, datetime.now())
        log.info("Kicking user=%s from group success", customer)
    return customer


def kick_group_members(trade_volumn=10000):
    url_kick = f"{c.TELEGRAM_API_PREFIX}/kickChatMember"
    url_unban = f"{c.TELEGRAM_API_PREFIX}/unbanChatMember"
    customers = customer_helper.get_all_customers_under_trade_valumn(trade_volumn)
    for customer in customers:
        params_kick = {
            "chat_id": c.VIP_GROUP_ID,
            "user_id": customer['tgid'],
            "until_date": int((time.time() + 10) * 1000)
        }
        # params_unban = {
        #     "chat_id": c.TEST_GROUP_ID,
        #     "user_id": customer['tgid'],
        # }
        requests.post(url_kick, params=params_kick)
        # requests.post(url_unban, params=params_unban)
        log.info("Kicking user=%s from group success", customer)
        update_customer_ban_status(customer['uid'], False, True, datetime.now())
    return customers


def set_member_whitelist(uid, is_whitelist):
    customer = customer_helper.update_customer_whitelist(uid, is_whitelist)
    return customer


def kick_all_zombies():
    url_kick = f"{c.TELEGRAM_API_PREFIX}/kickChatMember"
    customers = customer_helper.get_all_customers_in_group_chat()
    log.info("type=%s, c=%s", type(customers), customers)
    active_tgids = list(map(lambda x: str(x['tgid']), customers))
    log.info("count of actives=%s", len(active_tgids))
    tgids = customer_helper.get_all_tgids()
    for tgid in tgids:
        tgid = str(tgid)
        if tgid not in active_tgids:
            params_kick = {
                "chat_id": c.VIP_GROUP_ID,
                "user_id": tgid,
                "until_date": int((time.time() + 30) * 1000)
            }
            requests.post(url_kick, params=params_kick)
            # customer = customer_helper.get_customer_by_key("tgid", tgid)
            # if not customer['uid']:
            #     cus = get_customer_by_client_uid()
            #     customer_helper.save_customer(customer['uid'], customer['firstname'], customer['lastname'], tgid, )
            # customer_helper.update_customer_ban_status(customer['uid'], False, True, datetime.now())
            log.info("Kicking user with and tgid=%s success", tgid)

    return None


def update_customer_trade_volumn_scheduler():
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    today = datetime.now()
    last_month = today.replace(day=1) - dt.timedelta(days=1)
    epoch_ms = int(last_month.timestamp() * 1000)
    customers = customer_helper.get_all_customers()
    for customer in customers:
        params = {"uid": customer['uid'],
                  "startTime": str(epoch_ms),
                  "endTime": str(utils.get_timestamp()),
                  "pageNo": 1,
                  "pageSize": 1000
                  }
        response = request.post(c.VOLUMN_ENDPOINT, params)
        time.sleep(0.3)
        trade_list = response["data"] if response["data"] else None
        if not trade_list:
            return None
        total_volumn = utils.volumn_calculator(trade_list)
        log.info("total_volumn=%s", total_volumn)
        customer_helper.update_customer_volumn(customer['uid'], total_volumn)
    return None


def add_daily_trade_volumn_scheduler():
    customers = customer_helper.get_all_customers()
    for customer in customers:
        request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
        today = datetime.now()
        last_month = today.replace(day=1) - dt.timedelta(days=30)
        epoch_ms = int(last_month.timestamp() * 1000)
        params = {"uid": customer['uid'],
                  "startTime": str(epoch_ms),
                  "endTime": str(utils.get_timestamp()),
                  "pageNo": 1,
                  "pageSize": 1000
                  }
        response = request.post(c.VOLUMN_ENDPOINT, params)
        time.sleep(0.1)
        if response['data']:
            latest_trade = response['data'][-1]
            date = datetime.fromtimestamp(int(latest_trade['time'])/1000).strftime('%Y-%m-%d')
            uid = latest_trade['uid']
            volumn = latest_trade['volumn']
            customer_helper.save_daily_trade_volumn(uid, volumn, date)
            # log.info("info=%s, %s, %s ", date, uid, volumn)
            # cus_uid, cus_trade, trade_date = tuple_trade_info if tuple_trade_info else None
            log.info("adding customer daily trading volumn with uid=%s, volumn=%s, date=%s", uid, volumn, date)


def init_customer_trade_history():
    customers = customer_helper.get_all_customers()
    for customer in customers:
        request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
        today = datetime.now()
        last_month = today.replace(day=1) - dt.timedelta(days=30)
        epoch_ms = int(last_month.timestamp() * 1000)
        params = {"uid": customer['uid'],
                  "startTime": str(epoch_ms),
                  "endTime": str(utils.get_timestamp()),
                  "pageNo": 1,
                  "pageSize": 1000
                  }
        response = request.post(c.VOLUMN_ENDPOINT, params)
        time.sleep(0.1)
        if response['data']:
            trades = response['data']
            for trade in trades:
                date = datetime.fromtimestamp(int(trade['time']) / 1000).strftime('%Y-%m-%d')
                uid = trade['uid']
                volumn = trade['volumn']
                customer_helper.save_daily_trade_volumn(uid, volumn, date)
                log.info("init all customer trading history volumn with uid=%s, volumn=%s, date=%s", uid, volumn, date)
