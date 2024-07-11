import os
from pathlib import Path

import yaml

from dotenv import load_dotenv, find_dotenv
from typing import Final


load_dotenv(find_dotenv())
project_root = Path(__file__).parent.parent.parent

# Construct the path to the yaml file
resource_path = project_root / 'resource' / "application.yaml"


# def configure():
with open(resource_path, 'r') as f:
    config = yaml.safe_load(f)


APP_ID: Final = os.environ.get('APP_ID')
APP_HASH: Final = os.environ.get('APP_HASH')

# env variables
ENV: Final = os.environ.get('ENV')
TOKEN: Final = os.environ.get('TOKEN')
USERNAME: Final = os.environ.get('USERNAME')
ACCESS_KEY: Final = os.environ.get('ACCESS_KEY')
SECRET_KEY: Final = os.environ.get('SECRET_KEY')
PASSPHRASE: Final = os.environ.get('PASSPHRASE')

PORT: Final = config['server']['port']

# endpoint
BASE_URL: Final = config['service']['bit-get']['baseUrl']
AGENT_ENDPOINT: Final = config['service']['bit-get']['endpoint']['customer-list']
VOLUMN_ENDPOINT: Final = config['service']['bit-get']['endpoint']['customer-trade-volumn']
SERVER_TIME_ENDPOINT: Final = config['service']['bit-get']['endpoint']['server-time']

TELEGRAM_API_PREFIX: Final = f"{config['service']['telegram']['base-url']}bot{TOKEN}"

# http header
CONTENT_TYPE: Final = 'Content-Type'
OK_ACCESS_KEY: Final = 'ACCESS-KEY'
OK_ACCESS_SIGN: Final = 'ACCESS-SIGN'
OK_ACCESS_TIMESTAMP: Final = 'ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE: Final = 'ACCESS-PASSPHRASE'
APPLICATION_JSON: Final = 'application/json'

# header key
LOCALE: Final = 'locale'

# method
GET: Final = "GET"
POST: Final = "POST"
DELETE: Final = "DELETE"

# sign type
RSA: Final = "RSA"
SHA256: Final = "SHA256"
SIGN_TYPE: Final = SHA256

# database
DATABASE_NAME: Final = 'uidList_database.csv'
DBHOST: Final = config['service']['database']['host']
DBPORT: Final = config['service']['database']['port']
DBNAME: Final = config['service']['database']['dbname']
DB_USERNAME: Final = config['service']['database']['username']
DB_PASSWORD: Final = config['service']['database']['password']
DBHOST_PROD: Final = config['service']['database']['prod']['host']
DBPORT_PROD: Final = config['service']['database']['prod']['port']
DBNAME_PROD: Final = config['service']['database']['prod']['dbname']
DB_USERNAME_PROD: Final = config['service']['database']['prod']['username']
DB_PASSWORD_PROD: Final = config['service']['database']['prod']['password']

# tg group id
EFFECTIVE_CHAT_ID: Final = '-1002087737560'
VIP_GROUP_ID: Final = '-1001856345480'
# VIP_GROUP_ID: Final = config['service']['telegram']['test-group-id']
MAIN_GROUP_ID: Final = config['service']['telegram']['main-group-id']
# MAIN_GROUP_ID: Final = '-1002043576596'
PRIVATE_GROUP_ID: Final = '-1002043576596'
TEST_GROUP_ID: Final = config['service']['telegram']['test-group-id']

FINISH_CONVERSATION_MESSAGE: Final = """🦀已終止對話,感謝關注,祝您交易順利!📈"""

SUCCESS_MESSAGE_UID_CHECK: Final = """🦀您已驗證成功!感謝關注!✅"""
SUCCESS_MESSAGE_REJOIN: Final = """"""

ERROR_MESSAGE_FROM_BOT_REJOIN: Final = """❌未達入群資格,如有疑問請諮詢群主或管理🦀"""
ERROR_MESSAGE_FROM_BOT: Final = """❌UID不正確,本對話結束\n📲未在群裡的新會員請先輸入/join輸入會員資料\n📱已在群裡的老會員則先輸入/check輸入會員資料"""
ERROR_MESSAGE_FROM_BOT_USER_EXIST: Final = """☑️UID已驗證過,無須再次驗證,祝交易順利!📈"""
ERROR_MESSAGE_FROM_BOT_USER_BANNED: Final = """❌您因當月交易額未滿1萬u被移出群組\n""
                                            📈當交易額再次達到1萬u或一個月後\n
                                            ✅即可點選/rejoin重新加回\n
                                            🦀如有疑問請諮詢群主或管理,感謝使用,祝交易順利!"""
ERROR_MESSAGE_FROM_BOT_DUPLICATED_UID_CHECK: Final = """🦀您已驗證過,無須再次驗證!祝您交易順利!✅"""
