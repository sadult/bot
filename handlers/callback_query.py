
from strings import kb, steps, text
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from handlers import db
from handlers.message import account
import importlib
import sys

config = importlib.import_module('configs.'+sys.argv[0].split('.')[0])


def edit_information(update: Update, context: CallbackContext):
    '''Edit information of the user'''

    query = update.callback_query
    chat_id = update.effective_chat.id
    query.delete_message()
    r = context.bot.send_message(chat_id=chat_id,
                                 text=text.please_wait, reply_markup=kb.hide)
    r.delete()

    context.bot.send_message(chat_id=chat_id,
                             text=text.select_information, reply_markup=kb.select_information)

    query.answer()
    return steps.SELECT_INFORMATION


def edit_email(update: Update, context: CallbackContext):
    '''Edit Email of the user'''

    query = update.callback_query

    query.edit_message_text(
        text=text.edit_email, reply_markup=kb.back_select)

    query.answer()
    return steps.EDIT_EMAIL


def edit_twitter(update: Update, context: CallbackContext):
    '''Edit Twitter of the user'''

    query = update.callback_query

    query.edit_message_text(
        text=text.edit_twitter, reply_markup=kb.back_select)

    query.answer()
    return steps.EDIT_TWITTER


def edit_wallet(update: Update, context: CallbackContext):
    '''Edit Wallet of the user'''

    query = update.callback_query

    query.edit_message_text(
        text=text.edit_wallet, reply_markup=kb.back_select)

    query.answer()
    return steps.EDIT_WALLET


def back_account(update: Update, context: CallbackContext):
    '''Back to account information'''

    query = update.callback_query
    query.delete_message()
    query.answer()
    account(update, context, query.from_user.id)
    query.message.reply_text(text.home_menu, reply_markup=kb.home)
    return ConversationHandler.END


def back_select(update: Update, context: CallbackContext):
    '''Back to select information to edit menu'''

    query = update.callback_query
    query.edit_message_text(text=text.select_information,
                            reply_markup=kb.select_information)
    query.answer()

    return steps.SELECT_INFORMATION


def cb_continue(update: Update, context: CallbackContext):
    '''Send "Join the channel" message by clicking.'''

    query = update.callback_query
    query.edit_message_text(
        text=text.join_channel, reply_markup=kb.join_channel_with_done, disable_web_page_preview=True)

    query.answer()
    return steps.JOIN_CHANNEL


def check_join_channel(update: Update, context: CallbackContext):
    '''Check if the user has joined the channels.'''

    # return True
    query = update.callback_query
    channel1 = context.bot.get_chat_member(
        chat_id=f'@{config.CHANNEL1}', user_id=update.effective_chat.id)['status']
    # channel2 = context.bot.get_chat_member(
    #     chat_id='@'+config.CHANNEL1, user_id=update.effective_chat.id)['status']

    # Not joined
    L = ['left', 'kicked']
    if(channel1 in L): # or channel2 in L):
        query.answer(text.not_joined)
        return steps.JOIN_CHANNEL

    # Joined
    else:
        query.edit_message_text(
            text=text.follow_twitter, reply_markup=kb.follow_twitter, disable_web_page_preview=True)
        return steps.FOLLOW_TWITTER


def follow_twitter_done(update: Update, context: CallbackContext):
    '''Send "Enter your twitter username" message by clicking.'''

    query = update.callback_query
    query.edit_message_text(
        text=text.get_twitter_username)

    return steps.GET_TWITTER_USERNAME


def confirm_twitter_username(update: Update, context: CallbackContext):
    '''Send "Enter your Email" message by clicking.'''

    query = update.callback_query
    query.delete_message()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text.get_email)

    query.answer()
    return steps.GET_EMAIL


def confirm_email(update: Update, context: CallbackContext):
    '''Send "Enter your Wallet" message by clicking.'''

    query = update.callback_query
    query.delete_message()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text.get_wallet)

    query.answer()
    return steps.GET_WALLET


def confirm_wallet(update: Update, context: CallbackContext):
    '''Last step, Send "All tasks were completed" message by clicking.'''

    chat_id = update.effective_chat.id
    db.update(
        'users',
        f"status='active',balance=balance+{config.REGISTER_REWARD}",
        f'id={chat_id}')

    query = update.callback_query
    query.delete_message()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text.all_done, reply_markup=kb.home)

    # ? Send referral reward to referred_by
    referred_by = db.select('referred_by', 'users', f'id={chat_id}')
    if(referred_by and referred_by[0]['referred_by'] != None):
        referred_by = referred_by[0]['referred_by']
        context.bot.send_message(
            chat_id=referred_by, text=text.referral_joined.format(
                chat_id=referred_by, name=update.effective_chat.first_name).replace('[SYMBOL]', config.SYMBOL_UPPER).replace('[TOKENS]', config.REFERRAL_REWARD))
        db.update(
            'users',
            f"balance=balance+{config.REFERRAL_REWARD}",
            f'id={referred_by}')

    query.answer()


def withdraw_done(update: Update, context: CallbackContext):
    '''Send "Enter TXID: " message by clicking.'''

    query = update.callback_query
    query.delete_message()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text.get_wallet)

    query.answer()
    return steps.GET_WALLET

    return ConversationHandler.END


def error(update: Update, context: CallbackContext):
    '''Error callback for unknown callback queries.'''

    query = update.callback_query
    query.answer('Unknown Command!')
