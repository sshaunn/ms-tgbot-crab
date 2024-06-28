import datetime

import src.repository.customers_repository_helper as customer_helper
import requests

import src.common.constants as c
from src.bitget import utils
from src.bitget.bitget_api import BitgetApi as baseApi


def get_customers():
    url = f"{c.BASE_URL}{c.SERVER_TIME_ENDPOINT}"
    response = requests.get(url)
    customers = response.json()

    customer_helper.save_customer(101, "shaun", "shen", "101", "1710845728000")
    return customers


def get_customer_by_client_uid(uid):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    params = {"uid": uid,
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.AGENT_ENDPOINT, params)
    if not response["data"]:
        return None
    return response["data"][0]


def get_all_customers_by_client():
    """fucking stupid BITGET API, can only get 120 records, WTF is this shit.... ffs"""
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    today = datetime.datetime.now()
    last_month = today.replace(day=1) - datetime.timedelta(days=24 * 30)
    epoch_ms = int(last_month.timestamp() * 1000)
    params = {"startTime": str(epoch_ms),
              "endTime": str(utils.get_timestamp()),
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.AGENT_ENDPOINT, params)
    if not response:
        return None
    return {"length": len(response['data']), "details": response['data']}


def get_customer_trade_volumn_by_client_uid(uid):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    today = datetime.datetime.now()
    last_month = today.replace(day=1) - datetime.timedelta(days=1)
    epoch_ms = int(last_month.timestamp() * 1000)
    params = {"uid": uid,
              "startTime": str(epoch_ms),
              "endTime": str(utils.get_timestamp()),
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.VOLUMN_ENDPOINT, params)
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


def update_customer_trade_volumn(uid, volumn):
    customer = customer_helper.update_customer_volumn(uid, volumn)
    return customer


def update_customer_membership(uid, membership):
    customer = customer_helper.update_customer_membership(uid, membership)
    return customer


def update_customer_ban_status(uid, is_member, is_ban, left_time):
    customer = customer_helper.update_customer_ban_status(uid, is_member, is_ban, left_time)
    return customer


def update_customer_rejoin(uid, is_ban):
    customer = customer_helper.update_customer_rejoin(uid, is_ban)
    return customer
