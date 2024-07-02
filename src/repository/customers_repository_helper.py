import datetime

import src.config.datasource_config as dbconfig

from src.common.logger import log
from src.model.customers import Customer
from psycopg.errors import UniqueViolation
from src.bitget.utils import epoch_date_formater


def get_customer_by_uid(uid):
    try:
        record = dbconfig.fetch_cursor("""
        SELECT * FROM erp4btc.customers 
        WHERE uid=%s""", uid)
        if record:
            log.info("fetching customer by uid=%s, record=%s ", uid, record)
            return record
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer record with uid=%s, exception=%s", uid, ex)
        return None


def get_customer_like_uid(uid):
    pattern = f"%{uid}%"
    try:
        record = dbconfig.fetch_all_cursor_with_conditions("""
        SELECT * FROM erp4btc.customers 
        WHERE CAST(uid AS TEXT) LIKE %s""", (pattern,))
        if record:
            log.info("fetching customer by uid=%s, record=%s ", uid, record)
            return record
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer record with uid=%s, exception=%s", uid, ex)
        return None


# def get_all_customers_by_dates(trade_volumn):
#     try:
#         record = dbconfig.fetch_all_cursor_with_conditions("""
#         SELECT * FROM erp4btc.customers
#         WHERE CAST(uid AS TEXT) LIKE %s""", (pattern, ))
#         if record:
#             log.info("fetching customer by uid=%s, record=%s ", uid, record)
#             return record
#         else:
#             return None
#     except Exception as ex:
#         log.error("Error occurred when fetching customer record with uid=%s, exception=%s", uid, ex)
#         return None


def get_customer_by_key(keyname, value):
    try:
        record = dbconfig.fetch_cursor(
            f"SELECT uid, firstname, lastname, tgid, register_time FROM erp4btc.customers WHERE {keyname}=%s", value)
        if record:
            log.info(f"fetching customer by {keyname}=%s, record=%s", value, record)
            return record
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer record with %s=%s, exception=%s", keyname, value, ex)
        return None


def get_customer_ban_status_by_uid(uid):
    try:
        record = dbconfig.fetch_cursor("""
        SELECT uid, is_ban, left_time
        FROM erp4btc.customers 
        WHERE uid=%s""", uid)
        if record:
            log.info("fetching customer ban status by uid=%s, record=%s ", uid, record)
            return record
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer record with uid=%s, exception=%s", uid, ex)
        return None


def get_all_customers_under_trade_valumn(trade_volumn):
    try:
        records = dbconfig.fetch_all_cursor_with_conditions("""SELECT * FROM erp4btc.customers c 
        WHERE c.trade_volumn <= %s 
        AND c.is_whitelist = false""", (trade_volumn,))
        if isinstance(records, (list, tuple)):
            if records:
                log.info("Fetched %d customer records", len(records))
                return records
            else:
                log.info("No customer records found")
                return None
        elif isinstance(records, int):
            log.error("Received an integer instead of records. Value: %d", records)
            return None
        else:
            log.error("Unexpected type returned: %s", type(records))
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer records, exception=%s", ex)
        return None


def get_all_customers():
    try:
        records = dbconfig.fetch_all_cursor("SELECT * FROM erp4btc.customers c ORDER BY c.trade_volumn DESC")
        if records:
            log.info("fetching customer record=%s", records)
            return records
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer records, exception=%s", ex)
        return None


def save_customer(uid, firstname, lastname, tgid, register_time, is_member, is_whitelist, is_ban, join_time, left_time):
    formated_date = epoch_date_formater(register_time)
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, firstname, lastname, tgid, register_time, is_member, is_whitelist, is_ban, 
        join_time, left_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             uid, firstname, lastname, tgid, formated_date, is_member, is_whitelist, is_ban,
                             join_time, left_time)
        customer = Customer(uid, firstname, lastname, tgid, register_time, is_member, is_whitelist, is_ban, join_time,
                            left_time)
        log.info("saving customer record into database, customer=%s", customer.to_dict())
        return customer.to_dict()
    except UniqueViolation as uv:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, uv)
        return None
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_volumn(uid, volumn):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, trade_volumn) 
        VALUES (%s, %s) 
        ON CONFLICT (uid) DO UPDATE 
        SET trade_volumn=EXCLUDED.trade_volumn""", uid, volumn)
        return {"uid": uid, "trade_volumn": volumn, "message": "trade volumn updated success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_membership(uid, membership):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, is_member) 
        VALUES (%s, %s)
        ON CONFLICT (uid) DO UPDATE 
        SET is_member=EXCLUDED.is_member""", uid, membership)
        return {"uid": uid, "is_member": membership, "message": "membership updated success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_ban_status(uid, is_member, is_ban, left_time):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, is_member, is_ban, left_time) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (uid) DO UPDATE SET 
        is_member=EXCLUDED.is_member,
        is_ban=EXCLUDED.is_ban,
        left_time=EXCLUDED.left_time""", uid, is_member, is_ban, left_time)
        return {"uid": uid,
                "is_member": is_member,
                "is_ban": is_ban,
                "left_time": left_time,
                "message": "user banned success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_ban_status_by_tgid(tgid, is_member, is_ban, left_time):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (tgid, is_member, is_ban, left_time) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (tgid) DO UPDATE SET 
        is_member=EXCLUDED.is_member,
        is_ban=EXCLUDED.is_ban,
        left_time=EXCLUDED.left_time""", tgid, is_member, is_ban, left_time)
        return {"tgid": tgid,
                "is_member": is_member,
                "is_ban": is_ban,
                "left_time": left_time,
                "message": "user banned success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_rejoin(uid, is_ban):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, is_ban, is_member, left_time) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (uid) DO UPDATE SET 
        is_ban=EXCLUDED.is_ban,
        is_member=EXCLUDED.is_member,
        left_time=EXCLUDED.left_time""", uid, is_ban, True, datetime.datetime.now())
        return {"uid": uid, "is_ban": is_ban, "message": "user rejoin success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_whitelist(uid, is_whitelist):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, is_whitelist) 
        VALUES (%s, %s)
        ON CONFLICT (uid) DO UPDATE SET 
        is_whitelist=EXCLUDED.is_whitelist""", uid, is_whitelist)
        return {"uid": uid, "is_whitelist": is_whitelist, "message": "user whitelist setup success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def get_all_customers_in_group_chat():
    try:
        records = dbconfig.fetch_all_cursor("""SELECT * FROM erp4btc.customers WHERE is_member=True""")
        if records:
            return records
        return None
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def get_all_tgids():
    try:
        records = dbconfig.fetch_all_cursor("""SELECT * FROM erp4btc.customers WHERE is_member=True""")
        if records:
            return records
        return None
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def save_tgid(tgid):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.tgid1 (tgid) VALUES (%s)""", tgid)
        # log.info("saving customer record into database, customer=%s", customer.to_dict())
        return tgid
    except UniqueViolation as uv:
        log.error("Error occurred when inserting customer record with tgid=%s, and exception=%s", tgid, uv)
        return None
    except Exception as ex:
        log.error("Error occurred when inserting customer record with tgid=%s, and exception=%s", tgid, ex)
        return None
