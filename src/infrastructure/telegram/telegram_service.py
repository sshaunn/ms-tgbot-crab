import time

from telegram import Update, ChatMember, Bot
from telegram.ext import ContextTypes, ConversationHandler, Application
from telegram.error import TelegramError

import src.common.constants as c
import src.service.validation as vld
from src.bitget.utils import get_current_date
from src.common.logger import log
from datetime import datetime, date
from src.infrastructure.telegram.telegram_helper import extract_numeric_uid, create_group_invite_link
from src.service.customers_service import (get_customer_by_client_uid,
                                           save_customer,
                                           update_customer_membership,
                                           update_customer_ban_status,
                                           get_customer_by_key,
                                           get_customer_by_uid,
                                           update_customer_rejoin, update_customer_trade_volumn, update_customer_trade_volumn_by_client)

NEXT = range(1)


async def check_customer_uid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_type = update.message.chat.type
    message = update.message.text
    uid = extract_numeric_uid(message)
    customer = get_customer_by_client_uid(uid)

    if chat_type == 'private':

        if message == "/cancel":
            return ConversationHandler.END

        if not vld.is_valid_uid(customer):
            log.error("UID is not matching, user_id=%s, user_name=%s", user.id, user.first_name)
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT)
            return ConversationHandler.END

        customer = save_customer(uid,
                                 user.first_name,
                                 user.last_name,
                                 user.id,
                                 customer['registerTime'],
                                 join_time=get_current_date())

        update_customer_membership(uid, True)

        # if not customer:
        #     await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_DUPLICATED_UID_CHECK)
        #     await update.message.reply_text(c.FINISH_CONVERSATION_MESSAGE)
        #     return ConversationHandler.END

        # membership = await context.bot.get_chat_member(chat_id=c.VIP_GROUP_ID, user_id=user.id)
        # log.info("UID matching success, current user with UID=%s has membership=%s, and user=%s",
        #          uid,
        #          membership,
        #          customer)

        # if membership.status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]:
        #     update_customer_membership(uid, True)
        # update_customer_trade_volumn_by_client(uid)
        await update.message.reply_text(c.SUCCESS_MESSAGE_UID_CHECK)
        return ConversationHandler.END
    return ConversationHandler.END


async def start_customer_uid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_type = update.message.chat.type
    message = update.message.text
    uid = extract_numeric_uid(message)
    customer = get_customer_by_client_uid(uid)

    if chat_type == 'private':

        if message == "/cancel":
            return ConversationHandler.END

        if not vld.is_valid_uid(customer):
            log.error("UID is not matching, uid=%s, user_id=%s, user_name=%s", uid, user.id, user.first_name)
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT)
            return ConversationHandler.END

        # customer = get_customer_ban_status_by_uid(uid)
        # if customer['is_ban']:
        #     log.info("current user got banned, uid=%s, user_id=%s, user_name=%s", uid, user.id, user.first_name)
        #     await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_USER_BANNED)
        #     return ConversationHandler.END

        if vld.is_exist_uid(uid):
            log.error("UID is exist, uid=%s, user_id=%s, user_name=%s, customer=%s", uid, user.id, user.first_name, customer)
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_USER_EXIST)
            return ConversationHandler.END

        customer = save_customer(uid,
                                 user.first_name,
                                 user.last_name,
                                 user.id,
                                 customer['registerTime'],
                                 join_time=get_current_date())
        update_customer_trade_volumn_by_client(uid)
        invite_tuple = await create_group_invite_link(c.MAIN_GROUP_ID, c.VIP_GROUP_ID, context)
        inv_first, inv_sec = invite_tuple
        log.info("sending invite link to the user with uid=%s, user=%s", uid, customer)

        await update.message.reply_text(c.SUCCESS_MESSAGE_UID_CHECK)
        await update.message.reply_text(f"这是第一个邀请链接: {inv_first.invite_link}")
        await update.message.reply_text(f"这是第二个邀请链接: {inv_sec.invite_link}")
    return ConversationHandler.END


async def reinvite_customer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_type = update.message.chat.type
    message = update.message.text
    if chat_type == 'private':
        uid = extract_numeric_uid(message)
        if message == "/cancel":
            return ConversationHandler.END
        customer = get_customer_by_uid(uid)
        if not customer:
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_REJOIN)
            return ConversationHandler.END

        if not vld.is_over_trade_volumn(uid) and not vld.is_ban(customer['left_time']):
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_REJOIN)
            return ConversationHandler.END

        update_customer_rejoin(uid, False)
        invite_tuple = await create_group_invite_link(c.MAIN_GROUP_ID, c.VIP_GROUP_ID, context)
        log.info("sending invite link to the user with uid=%s, user=%s", uid, customer)
        inv_first, inv_sec = invite_tuple
        await update.message.reply_text(c.SUCCESS_MESSAGE_UID_CHECK)
        await update.message.reply_text(f"🍍鳳梨屋交流群邀請連結: {inv_first.invite_link}")
        await update.message.reply_text(f"🪣海之霸VIP群邀請連結: {inv_sec.invite_link}")
        return ConversationHandler.END


async def check_customer_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]:
        new_member = result.new_chat_member.user
        customer = get_customer_by_key('tgid', str(new_member.id))
        if customer:
            update_customer_membership(customer['uid'], True)
            log.info("current user with UID=%s, tgid=%s has membership", customer['uid'], new_member.id)


async def check_trade_volumn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_type = update.message.chat.type
    message = update.message.text
    uid = extract_numeric_uid(message)
    customer = get_customer_by_client_uid(uid)
    cus = get_customer_by_uid(uid)
    if message == "/cancel":
        return ConversationHandler.END
    if chat_type == 'private':
        if message == "/cancel":
            return ConversationHandler.END

        if not vld.is_valid_uid(customer) and not cus:
            log.error("UID is not matching, uid=%s, user_id=%s, user_name=%s", uid, user.id, user.first_name)
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT)
            return ConversationHandler.END

        today_date = datetime.now()
        today = int(time.time() * 1000)
        first_day_of_month = int(datetime.combine(date(today_date.year, today_date.month, 1), datetime.min.time()).timestamp() * 1000)

        c = update_customer_trade_volumn(uid, first_day_of_month, today)
        if c:
            await update.message.reply_text(f"🔎查詢成功,距離本月1號到今日,您的交易額為:{c['trade_volumn']}")
            return ConversationHandler.END
    await update.message.reply_text(f"❌查詢失敗請重試")
    return ConversationHandler.END


async def kick_group_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        uid = extract_numeric_uid(update.message.text)
        chat_id = c.VIP_GROUP_ID

        customer = get_customer_by_uid(uid)
        if not customer:
            log.error("current user with uid=%s not found", uid)
            return NEXT

        await context.bot.ban_chat_member(chat_id, customer['tgid'])
        await context.bot.unban_chat_member(chat_id, customer['tgid'])

        if customer:
            update_customer_ban_status(uid, False, True, get_current_date())
            log.info("current user with UID=%s, tgid=%s cancelled membership", uid, customer['tgid'])
    except ValueError:
        await update.message.reply_text('Please send a valid user ID.')
    except Exception as e:
        log.error(f'Error kicking user: {e}')
        await update.message.reply_text('An error occurred while trying to kick the user.')
    return ConversationHandler.END


async def send_heartbeat(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message("-1002217128790", text="heartbeat")


# Usage
# chat_id = -1001234567890  # Replace with your group chat ID
# member_ids = app.run(get_all_members(chat_id))
# print(member_ids)