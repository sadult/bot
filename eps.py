import html
import json
import logging
import os
import traceback
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.defaults import Defaults
from telegram.parsemode import ParseMode
from telegram.update import Update

from handlers import callback_query, command, message
from strings import steps, btn
from configs import eps as config  # ! Important

logging.basicConfig(
    format='[%(levelname)s][%(asctime)s](%(name)s) : %(message)s', level=logging.INFO, datefmt="%m-%d %H:%M")  # %Y-:%S
logger = logging.getLogger(__name__)


def main():
    os.system('clear')
    print(config.SYMBOL+" Airdrop Bot Started.")

    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(config.TOKEN, defaults=defaults)
    dp = updater.dispatcher

    # ? Sudo Commands
    for cmd in ['sql', 'shell', 'withdraw', 'users', 'stats', 'delete_db', 'restart', 'commands']:
        callback = getattr(command, cmd)
        dp.add_handler(CommandHandler(
            cmd, callback, Filters.chat_type.private & Filters.user(config.SUDO)))

    # ? User commands
    dp.add_handler(CommandHandler(
        'faq', message.faq, Filters.chat_type.private))

    # ? Conversation Handlers

    # Edit information
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                callback_query.edit_information, pattern='^edit_information$')],
        states={
            steps.SELECT_INFORMATION: [
                CallbackQueryHandler(
                    callback_query.edit_email, pattern='^edit_email$'),
                CallbackQueryHandler(
                    callback_query.edit_twitter, pattern='^edit_twitter$'),
                CallbackQueryHandler(
                    callback_query.edit_wallet, pattern='^edit_wallet$'),
                CallbackQueryHandler(
                    callback_query.back_account, pattern='^back_account$'),
            ],
            steps.EDIT_EMAIL: [
                MessageHandler(Filters.chat_type.private,
                               callback=message.edit_email),
                CallbackQueryHandler(
                    callback_query.back_select, pattern='^back_select$'),
            ],
            steps.EDIT_TWITTER: [
                MessageHandler(Filters.chat_type.private,
                               callback=message.edit_twitter),
                CallbackQueryHandler(
                    callback_query.back_select, pattern='^back_select$'),
            ],
            steps.EDIT_WALLET: [
                MessageHandler(Filters.chat_type.private,
                               callback=message.edit_wallet),
                CallbackQueryHandler(
                    callback_query.back_select, pattern='^back_select$'),
            ],
        },
        fallbacks=[CommandHandler('error', command.error)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    # Withdraw request
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                Filters.chat_type.private & Filters.regex(f'^{btn.withdraw}$'), message.withdraw)],
        states={
            steps.GET_TXID: [
                MessageHandler(Filters.chat_type.private,
                               callback=message.get_txid)]
        },
        fallbacks=[CommandHandler('error', command.error)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            command='start', callback=command.start, filters=Filters.chat_type.private)],
        states={
            steps.START_REGISTERING: [
                CallbackQueryHandler(
                    callback_query.cb_continue, pattern='^continue$')
            ],
            steps.JOIN_CHANNEL: [
                CallbackQueryHandler(
                    callback_query.check_join_channel, pattern='^check_join_channel$')
            ],
            steps.FOLLOW_TWITTER: [
                CallbackQueryHandler(
                    callback_query.follow_twitter_done, pattern='^follow_twitter_done$'),
            ],
            steps.GET_TWITTER_USERNAME: [
                MessageHandler(
                    Filters.chat_type.private & Filters.text, callback=message.get_twitter_username),
            ],
            steps.CONFIRM_TWITTER_USERNAME: [
                CallbackQueryHandler(
                    callback_query.confirm_twitter_username, pattern='^confirm_twitter_username$'),
            ],
            steps.GET_EMAIL: [
                MessageHandler(
                    Filters.chat_type.private & Filters.text, message.get_email)
            ],
            steps.CONFIRM_EMAIL: [
                CallbackQueryHandler(
                    callback_query.confirm_email, pattern='^confirm_email$'),
            ],
            steps.GET_WALLET: [
                MessageHandler(
                    Filters.chat_type.private & Filters.text, message.get_wallet)
            ],
            steps.CONFIRM_WALLET: [
                CallbackQueryHandler(
                    callback_query.confirm_wallet, pattern='^confirm_wallet$'),
            ],
        },
        fallbacks=[CommandHandler('error', command.error)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    # Send to all
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            command='s2a', callback=command.send_to_all, filters=Filters.chat_type.private & Filters.user(config.SUDO))],
        states={
            steps.GET_S2A_ALL: [
                MessageHandler(
                    Filters.chat_type.private & Filters.user(config.SUDO), callback=message.get_s2a),
            ],
        },
        fallbacks=[CommandHandler('error', command.error)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    # Send to all
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            command='s2nr', callback=command.send_to_not_registered, filters=Filters.chat_type.private & Filters.user(config.SUDO))],
        states={
            steps.GET_S2A_NR: [
                MessageHandler(
                    Filters.chat_type.private & Filters.user(config.SUDO), callback=message.get_s2nr),
            ],
        },
        fallbacks=[CommandHandler('error', command.error)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    # Send to all
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            command='s2r', callback=command.send_to_registered, filters=Filters.chat_type.private & Filters.user(config.SUDO))],
        states={
            steps.GET_S2A_NR: [
                MessageHandler(
                    Filters.chat_type.private & Filters.user(config.SUDO), callback=message.get_s2r),
            ],
        },
        fallbacks=[CommandHandler('error', command.error)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    # ? Message Handlers
    dp.add_handler(MessageHandler(
        Filters.chat_type.private, callback=message.handler))

    # Error Handlers
    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


def error_handler(update: Update, context: CallbackContext):
    logger.error(msg="Error happend:",
                 exc_info=context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = '\n'.join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update:\n\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
    context.bot.send_message(chat_id=config.SUDO, text=message)


if __name__ == '__main__':
    main()
