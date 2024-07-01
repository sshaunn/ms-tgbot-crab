import customers_service as cs


def volumn_calculator(trades):
    total_volumn = 0
    for trade in trades:
        total_volumn += float(trade['volumn'])
    return total_volumn
