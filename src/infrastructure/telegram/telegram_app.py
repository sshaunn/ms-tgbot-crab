#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from src.common.logger import log
import src.common.constants as c
import src.service.validation as vld

from src.infrastructure.telegram.telegram_helper import conversation_handler
from src.infrastructure.telegram.telegram_service import (check_customer_uid_command,
                                                          start_customer_uid_command,
                                                          check_customer_membership,
                                                          kick_group_member,
                                                          reinvite_customer,
                                                          send_heartbeat,
                                                          check_trade_volumn)
from telegram import ForceReply, Update, ChatMember, ReplyKeyboardMarkup
from telegram.ext import (CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          filters,
                          ConversationHandler,
                          ChatMemberHandler,
                          Application)

UID = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"🦀≡≡≡≡≡≡≡≡▷►◈◄◁≡≡≡≡≡≡≡≡🦀\n\n"
        "🔝歡迎各位加入🪣比奇堡海之霸VIP🔇\n"
        "因我個人的策略關係，(槓桿高，盈虧比高)📈\n"
        "有些訂單接受度較低，在大群發布容易被噴\n"
        "因此簡單設立一個門檻，避免路人粉瞎操作爆倉\n"
        "加上之後會有獎勵活動避免註冊後白嫖\n"
        "每個月最低10000u交易量(含槓桿)"
        "非常低的標準，每月1號核對\n\n"
        "內容：\n"
        "🅰️最高20%合約20+20%現貨手續費減免✨\n"
        "🅱️專屬團隊bitget跟單服務\n"
        "⚡️VIP群高盈虧比策略分享\n"
        "🧽交流群加入資格\n"
        "加入步驟：\n"
        "1️⃣點擊連結註冊帳號⭐️\n"
        "https://partner.bitget.fit/bg/MrKrabs\n"
        "2️⃣發送UID給機器人確認♥️\n"
        "https://t.me/wedjatbtcVIP_bot\n"
        "⚠️邀請連結為一次性使用⚠️\n"
        "⚠️註冊後記得點擊下方加入在退出⚠️\n"
        "⚠️否則無法再次點擊⚠️\n\n"
        "⚠️以下是不同会员入群命令以及交易额查询⚠️\n\n"
        "/rejoin - 若之前交易额不满足要求将会被移除VIP群 重新加群请输入此命令\n"
        "/volume - 交易总额查询 请输入此命令\n"
        "/check - 老会员信息录入请输入此命令\n"
        "/join - 新加群会员请输入此命令\n\n"
        "若有任何疑问请直接私讯我本人谢谢\n"
        "🦀≡≡≡≡≡≡≡≡▷►◈◄◁≡≡≡≡≡≡≡≡🦀"
    )

    # Create keyboard layout
    keyboard = [
        ['/rejoin', '/volume'],
        ['/check', '/join']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("开始验证Bitget-UID,请输入你的数字UID,或者输入/cancel退出验证:")
    return UID


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    log.info("User with id=%s, name=%s canceled the conversation.", user.id, user.first_name)
    await update.message.reply_text('您已终止对话,感谢关注,祝您交易顺利!')
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def bot_app():
    """Start the bot."""
    application = Application.builder().token(c.TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conversation_handler(check, check_customer_uid_command, cancel, UID, 'check'))
    application.add_handler(conversation_handler(check, start_customer_uid_command, cancel, UID, 'join'))
    application.add_handler(conversation_handler(check, check_trade_volumn, cancel, UID, 'volume'))
    application.add_handler(conversation_handler(check, kick_group_member, cancel, UID, 'kick'))
    application.add_handler(conversation_handler(check, reinvite_customer, cancel, UID, 'rejoin'))
    application.add_handler(ChatMemberHandler(check_customer_membership, ChatMemberHandler.CHAT_MEMBER))
    application.job_queue.run_repeating(send_heartbeat, interval=1800, first=1800)
    # check_conversation_handler()
    #
    # # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))
    #
    # # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_customer_command))
    # return application
    # application.start()
    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # return application
