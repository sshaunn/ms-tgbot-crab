import logging
import psycopg
import src.common.constants as c

from psycopg.rows import class_row, dict_row


def get_db_connection():
    conn = psycopg.connect(f"host={c.DBHOST} dbname={c.DBNAME} user={c.DB_USERNAME} password={c.DB_PASSWORD}",
                           row_factory=dict_row)
    return conn


def exec_cursor(sql_query, *values):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, values)
        conn.commit()
        conn.close()


def fetch_cursor(sql_query, *values):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, values)
            record = cur.fetchone()
            conn.close()
        return record


def fetch_all_cursor(sql_query):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            record = cur.fetchall()
            conn.close()
        return record
