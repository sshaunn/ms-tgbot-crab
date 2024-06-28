from datetime import datetime, date

from src.service.customers_service import get_customer_by_uid


def is_valid_uid(customer):
    return customer is not None


def is_exist_uid(uid):
    customer = get_customer_by_uid(uid)
    return customer is not None and not customer['is_ban'] and customer['is_member']


def can_rejoin(start_time):
    start_date = datetime.strptime(start_time.isoformat(), "%Y-%m-%d").date()
    return (date.today() - start_date).days < 30
