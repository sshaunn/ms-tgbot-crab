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
from telegram import ForceReply, Update, ChatMember
from telegram.ext import (CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          filters,
                          ConversationHandler,
                          ChatMemberHandler,
                          Application)

UID = range(2)


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("开始验证Bitget-UID,请输入你的数字UID:")
    return UID


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    log.info(20, "User with id=%s, name=%s canceled the conversation.", user.id, user.first_name)
    await update.message.reply_text('您已终止对话,感谢关注,祝您交易顺利!')
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def bot_app():
    """Start the bot."""
    application = Application.builder().token(c.TOKEN).build()
    application.add_handler(conversation_handler(check, check_customer_uid_command, cancel, UID, 'check'))
    application.add_handler(conversation_handler(check, start_customer_uid_command, cancel, UID, 'start'))
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
