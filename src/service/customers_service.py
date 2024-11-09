import time
import datetime as dt
import src.repository.customers_repository_helper as customer_helper
import requests

import src.common.constants as c
from datetime import datetime
from src.common.logger import log
from src.bitget import utils
from src.bitget.bitget_api import BitgetApi as baseApi
from src.repository.customers_repository_helper import get_all_customers

user_id_list = [
    "206120298",
    "7105163019",
    "5610667768",
    "7158902603",
    "6239698090",
    "1891622309",
    "6441579644",
    "7128925336",
    "1899111034",
    "5253264407",
    "6816787625",
    "6640091388",
    "6798413327",
    "378160546",
    "1853600594",
    "6830079595",
    "2138866166",
    "6439323573",
    "2022678308",
    "6950484725",
    "5246738817",
    "5224160925",
    "6228716352",
    "7265450257",
    "6782937614",
    "5555724150",
    "7192353302",
    "5545509164",
    "5980831466",
    "6312088842",
    "7209964299",
    "1004136440",
    "6010952958",
    "5216088421",
    "2117810979",
    "1744341433",
    "5373928889",
    "5375690394",
    "6232959984",
    "1319512808",
    "1737264508",
    "1008123877",
    "6632987338",
    "1770885290",
    "5690534511",
    "5250879837",
    "7161995890",
    "6057079982",
    "6201162960",
    "2042887075",
    "6712632926",
    "5997073821",
    "6688487099",
    "5456702448",
    "6691351011",
    "6843010877",
    "6759954879",
    "6464504079",
    "7052469295",
    "1038854609",
    "7458480143",
    "5823863629",
    "6177409410",
    "6221408408",
    "6339774326",
    "978532801",
    "5022329854",
    "6510238553",
    "7122459295",
    "6415208312",
    "5853051657",
    "6453939479",
    "6934457962",
    "7076070880",
    "854503183",
    "5068829454",
    "5399043761",
    "1430184427",
    "1761214598",
    "7141624538",
    "6170085972",
    "6491618985",
    "1818905550",
    "1304732093",
    "1149991161",
    "6783950347",
    "5238813893",
    "5713267280",
    "6290340132",
    "7020864922",
    "7364222633",
    "1608667232",
    "6090442528",
    "5312536167",
    "536533191",
    "1620338387",
    "1213080811",
    "6062619983",
    "6176142798",
    "6296508739",
    "6843614734",
    "5254379841",
    "1165377013",
    "6553049970",
    "1481453172",
    "7081952964",
    "6728896845",
    "6590508334",
    "1797273077",
    "5390946529",
    "6757730218",
    "7004986876",
    "6421763712",
    "1307610568",
    "1518037134",
    "7316305327",
    "1329427683",
    "5577388667",
    "894918717",
    "6940408838",
    "6637408512",
    "7388016321",
    "7101848345",
    "6440883041",
    "7085761697",
    "1394473270",
    "7512884712",
    "1081847742",
    "6916519136",
    "7003645898",
    "1200514231",
    "1831160942",
    "5917069188",
    "6970723909",
    "5213828874",
    "7134779831",
    "6144173150",
    "5899289878",
    "1799379567",
    "6656703888",
    "7072730164",
    "7478297924",
    "7035103483",
    "6947568740",
    "6261980433",
    "6883839268",
    "7405929566",
    "7141542460",
    "1861450174",
    "7134756300",
    "5250727377",
    "5272200672",
    "1906633903",
    "5259543879",
    "6869986970",
    "6163153758",
    "6249076481",
    "1837384121",
    "7065242259",
    "5459287822",
    "7120990072",
    "6041035790",
    "253705585",
    "6757446485",
    "1779462083",
    "6235435378",
    "805694260",
    "644663332",
    "858147078",
    "1793774697",
    "1090481032",
    "1373758202",
    "6656871459",
    "6349582554",
    "5009276646",
    "7434172618",
    "6795543206",
    "6766329744",
    "7149654745",
    "1783497463",
    "6932623341",
    "5757273188",
    "6213302263",
    "5620671585",
    "1837104907",
    "5408383209",
    "6211719444",
    "1371757657",
    "1351402847",
    "7251049359",
    "1776648755",
    "5189271951",
    "713430818",
    "1077384174",
    "6907646660",
    "7159957575",
    "2107193908",
    "1568528738",
    "5198933670",
    "1830843054",
    "6317522133",
    "5054449938",
    "6881431478",
    "5341443579",
    "5418383550",
    "1639171776",
    "1884677991",
    "6807288487",
    "7246938182",
    "7232366117",
    "1165955007",
    "7512569111",
    "6558282391",
    "5890462268",
    "5061248554",
    "5174407251",
    "6822406747",
    "1298935951",
    "584314835",
    "6530799803",
    "1620817878",
    "7185537224",
    "6550558640",
    "5897502807",
    "6512246255",
    "6775407103",
    "6887019422",
    "1192745560",
    "1684887392",
    "5413768116",
    "5373928889",
    "6439342210",
    "6293689105",
    "5999607505",
    "5337076358",
    "5147625806",
    "1991514068",
    "6147041518",
    "5201663332",
    "5071111573",
    "5764210587",
    "1057996935",
    "6291943595",
    "6111400782",
    "6214473437",
    "1331014413",
    "6873684828",
    "5756761987",
    "7058385089",
    "7082923497",
    "5230598482",
    "6353073272",
    "6914318688",
    "1245006754",
    "5075513546",
    "5032746390",
    "2006338232",
    "1451009370",
    "6848524503",
    "803496284",
    "5103905475",
    "5816709590",
    "1092010302",
    "5729501747",
    "6145571428",
    "1164503191",
    "7144913576",
    "7382777032",
    "1757063062",
    "6244257039",
    "1177628503",
    "1991186245",
    "6873684828",
    "7100385484",
    "6368102064",
    "845669133",
    "1231856298",
    "1490347247",
    "959930045",
    "5373928889",
    "5540910956",
    "1820018705",
    "6224254867",
    "1872142920",
    "5690587694",
    "6719008022",
    "7729366503",
    "6223895205",
    "7463401858",
    "6767967806",
    "5483221129",
    "5550397041",
    "5333117457",
    "6817102209",
    "7519596053",
    "6367002128",
    "1479093973",
    "6002891515"
]

left_ids = [
    "7158902603",
    "6239698090",
    "1899111034",
    "1853600594",
    "6632987338",
    "1770885290",
    "6510238553",
    "6415208312",
    "5853051657",
    "6934457962",
    "7076070880",
    "1430184427",
    "1761214598",
    "6170085972",
    "1818905550",
    "1304732093",
    "6090442528",
    "536533191",
    "1620338387",
    "6062619983",
    "1797273077",
    "6757730218",
    "1329427683",
    "5577388667",
    "6916519136",
    "1200514231",
    "7134779831",
    "5899289878",
    "1799379567",
    "6656703888",
    "7072730164",
    "7478297924",
    "6261980433",
    "1861450174",
    "7065242259",
    "7120990072",
    "6757446485",
    "644663332",
    "1373758202",
    "6656871459",
    "6349582554",
    "5009276646",
    "7434172618",
    "6795543206",
    "6932623341",
    "5408383209",
    "7251049359",
    "713430818",
    "1077384174",
    "7159957575",
    "2107193908",
    "1568528738",
    "1830843054",
    "7232366117",
    "6558282391",
    "6530799803",
    "1620817878",
    "7185537224",
    "6512246255",
    "6887019422",
    "1192745560",
    "5337076358",
    "5147625806",
    "1991514068",
    "6147041518",
    "5201663332",
    "6111400782",
    "6873684828",
    "5032746390",
    "1451009370",
    "6145571428",
    "7144913576",
    "6244257039",
    "6873684828",
    "6368102064",
    "845669133",
    "5540910956",
    "6224254867",
    "5690587694"
]

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
    customers = get_all_customers()
    cus_list=[]
    # if uid:
    #     params = {"uid": uid,
    #               "startTime": str(1727740800),
    #               "endTime": str(1730591999),
    #               "pageNo": 1,
    #               "pageSize": 1000
    #               }
    #     response = request.post(c.VOLUMN_ENDPOINT, params)
    #     if not response["data"]:
    #         return None
    #     return sum(map(lambda d: float(d["volumn"]), response["data"]))
    for customer in customers:
        params = {"uid": customer["uid"],
                  "startTime": str(1727740800),
                  "endTime": str(1730591999),
                  "pageNo": 1,
                  "pageSize": 1000
                  }
        response = request.post(c.VOLUMN_ENDPOINT, params)
        time.sleep(0.2)
        if not response["data"]:
            return None
        v = sum(map(lambda d: float(d["volumn"]), response["data"]))
        if v > 0:
            cus_list.append(f"{customer["tgid"]}")
            print(customer["uid"], customer["tgid"], "volumn= ", v)
    return cus_list


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
        params_kick_main = {
            "chat_id": c.MAIN_GROUP_ID,
            "user_id": customer['tgid'],
            "until_date": int((time.time() + 10) * 1000)
        }
        # params_unban = {
        #     "chat_id": c.TEST_GROUP_ID,
        #     "user_id": customer['tgid'],
        # }
        requests.post(url_kick, params=params_kick)
        requests.post(url_kick, params=params_kick_main)
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

def hotfix():
    # "https://t.me/+p8JO8MDefFllODU1"
    # "https://t.me/+kpMKL6L5nldkNjQ1"
    # url = "https://api.telegram.org/bot6686723471:AAEE7vOHZIm-D7txgrGtA2M2swLBt-m-rZU/sendMessage"
    url = "https://api.telegram.org/bot6686723471:AAEE7vOHZIm-D7txgrGtA2M2swLBt-m-rZU/getChatMember"
    # url = "https://api.telegram.org/bot6686723471:AAEE7vOHZIm-D7txgrGtA2M2swLBt-m-rZU/unbanChatMember"
    # p = {
    #     "chat_id": "7095291840",
    #     "text": "抱歉我是蟹老板的傻逼技\n由于我的失误导致误删\n抱歉\n这个是VIP邀请链接:\n https://t.me/+p8JO8MDefFllODU1"
    # }
    # p1 = {
    #     "chat_id": "7095291840",
    #     "text": "抱歉我是蟹老板的傻逼技术\n由于我的失误导致误删\n被长抱歉\n这个是交流群邀请链接:\n https://t.me/+kpMKL6L5nldkNjQ1"
    # }
    # p2 = {
    #     "chat_id": user_id,
    #     "text": "邀请链接后台已生效 可重新点击邀请连接入群"
    # }
    # customers = get_all_customers()
    reses = []

    # for left_id in left_ids:
    #     left_id = str(left_id)
    #     reses.append(left_id)

    for user_id in left_ids:
    # for user_id in user_id_list:
    # for customer in customers:
        p = {
            "chat_id": c.MAIN_GROUP_ID,
            "user_id": user_id,
        }
    #     p = {
    #         "chat_id": user_id,
    #         "text": "VIP邀请链接:\n https://t.me/+opzfggWFYs9lODRl"
    #     }
    #     p1 = {
    #         "chat_id": user_id,
    #         "text": "交流群邀请链接:\n https://t.me/+xTouhDqKZwk3NWZl"
    #     }
    #     p2 = {
    #         "chat_id": user_id,
    #         "text": "邀请链接后台已生效 可重新点击邀请连接入群"
    #     }
        # p = {
        #     "chat_id": c.VIP_GROUP_ID,
        #     "user_id": customer['tgid']
        # }
        # p1 = {
        #     "chat_id": c.MAIN_GROUP_ID,
        #     "user_id": customer['tgid'],
        # }

        res = requests.post(url, params=p)
        data = res.json()
        if data["result"]["status"] == "left":
            # userid = data["result"]["user"]["id"]
            reses.append(data)
        # requests.post(url, params=p)
        # requests.post(url, params=p1)
        # requests.post(url, params=p2)
    return reses
    # return reses