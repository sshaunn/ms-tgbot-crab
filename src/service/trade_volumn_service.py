import customers_service as cs


def volumn_calculator(uid):
    total_volumn = 0
    trades = cs.get_customer_trade_volumn_by_client_uid(uid)
    for trade in trades:
        total_volumn += float(trade['volumn'])
    return total_volumn
