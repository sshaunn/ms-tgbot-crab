from psycopg.errors import UniqueViolation

import src.config.datasource_config as dbconfig
from src.common.logger import log


def save_admin(username, password):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.admin (username, password) VALUES (%s, %s)""",
                             username, password)
        log.info("saving customer record into database, admin=%s", {username, password})
        return {username, password}
    except UniqueViolation as uv:
        log.error("Error occurred when inserting customer record with username=%s, and exception=%s", username, uv)
        return None
    except Exception as ex:
        log.error("Error occurred when inserting customer record with username=%s, and exception=%s", username, ex)
        return None


def get_admin(user, password):
    try:
        record = dbconfig.fetch_cursor("""
        SELECT username, password FROM erp4btc.admin 
        WHERE username=%s
        AND password=%s""", user, password)
        if record:
            log.info("fetching admin by user=%s, record=%s ", user, record)
            return record
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer record with username=%s, exception=%s", user, ex)
        return None
