import importlib
import sys
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import validators
from strings import btn, kb, steps, text
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from handlers import db

config = importlib.import_module('configs.'+sys.argv[0].split('.')[0])


def handler(update: Update, context: CallbackContext):
    '''Handler of all messages'''

    # Get full name of the user
    full_name = update.effective_chat.first_name
    if(update.effective_chat.last_name):
        full_name = full_name+' '+update.effective_chat.last_name

    # Get user information from DB
    user = db.create_user(chat_id=update.effective_chat.id, name=full_name)

    # Text that entered by the user
    user_text = update.message.text

    # ? If the user has already completed all his tasks.
    if(user['status'] == 'active'):

        joined = check_join_channel(update, context)
        if(joined):

            if user_text == btn.balance:
                balance(update, context)

            elif user_text == btn.withdraw:
                withdraw(update, context)

            elif user_text == btn.account:
                account(update, context)

            elif user_text == btn.referral:
                referral(update, context)

            elif user_text == btn.faq:
                faq(update, context)

            else:
                error(update, context)
    # TODO:
    # else:
        # update.message.reply_text(text.unknown_problem, reply_markup=kb.hide)


def get_s2a(update: Update, context: CallbackContext):
    '''Get the "send_to_all" message and send it to all users'''

    if(update.message.text == btn.backtohome):
        update.message.reply_text(text.home_menu, reply_markup=kb.home)
    else:
        users = db.select('id', 'users')
        sent = 0
        total_users = len(users)

        for user in users:
            try:
                context.bot.send_message(
                    chat_id=user['id'], text=update.message.text)
                sent += 1
            except:
                continue

        update.message.reply_text(
            f"✅ <b>Your message was sent to {sent} users (of {total_users}).</b>", reply_markup=kb.home)
    return ConversationHandler.END


def get_s2nr(update: Update, context: CallbackContext):
    '''Get the "send_to_not_registered" message and send it to not registered users'''

    if(update.message.text == btn.backtohome):
        update.message.reply_text(text.home_menu, reply_markup=kb.home)
    else:
        users = db.select('id', 'users', "status='registering'")
        sent = 0
        total_users = len(users)

        for user in users:
            try:
                context.bot.send_message(
                    chat_id=user['id'], text=update.message.text)
                sent += 1
            except:
                continue

        update.message.reply_text(
            f"✅ <b>Your message was sent to {sent} users (of {total_users}).</b>", reply_markup=kb.home)
    return ConversationHandler.END


def get_s2r(update: Update, context: CallbackContext):
    '''Get the "send_to_registered" message and send it to not registered users'''

    if(update.message.text == btn.backtohome):
        update.message.reply_text(text.home_menu, reply_markup=kb.home)
    else:
        users = db.select('id', 'users', "status='active'")
        sent = 0
        total_users = len(users)

        for user in users:
            try:
                context.bot.send_message(
                    chat_id=user['id'], text=update.message.text)
                sent += 1
            except:
                continue

        update.message.reply_text(
            f"✅ <b>Your message was sent to {sent} users (of {total_users}).</b>", reply_markup=kb.home)
    return ConversationHandler.END


def get_txid(update: Update, context: CallbackContext):
    '''Get TXID [DONE]'''

    if(update.message.text in [btn.back, '/start']):
        update.message.reply_text(text.home_menu, reply_markup=kb.home)
    else:
        user_text = update.message.text
        if(len(user_text) > 10):
            full_name = update.effective_chat.first_name
            if(update.effective_chat.last_name):
                full_name = full_name+' '+update.effective_chat.last_name
            chat_id = str(update.effective_chat.id)
            user = db.select('*', 'users', f'id={chat_id}')[0]

            t = text.withdraw_done_channel.format(
                full_name=full_name,
                chat_id=chat_id[:-3]+'***',
                symbol=config.SYMBOL_UPPER,
                tokens=user['balance'],
                wallet=user['wallet'],
                usd=str(
                    int(float(user['balance'])*float(config.CURRENT_PRICE))),
                # txid=user_text,
                channel=config.CHANNEL1,
            )

            r = context.bot.send_message(chat_id='@'+config.CHANNEL1, text=t,disable_web_page_preview=True)

            # db.update('users', 'balance=0', f'id={chat_id}')

            kb_check = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text=btn.check, url=f'https://t.me/{config.CHANNEL1}/{r.message_id}')
                ]
            ])

            update.message.reply_text(
                text=text.withdraw_done.format(
                    tokens=0, usd=0, symbol=config.SYMBOL_UPPER),
                reply_markup=kb_check, disable_web_page_preview=True)

            update.message.reply_text(
                text=text.home_menu, reply_markup=kb.home)
        else:
            update.message.reply_text(text.txid_error)
            return steps.GET_TXID
    return ConversationHandler.END


def get_twitter_username(update: Update, context: CallbackContext):
    '''Get the user's twitter username'''

    t = update.message.text
    chat_id = update.effective_chat.id

    # ? Username must be at least 4 characters long.
    if(len(t) >= 4 and t.startswith('@') == False):
        db.update(
            'users',
            f"twitter='{t}'",
            f'id={chat_id}')

        update.message.reply_text(
            text.confirm_twitter_username.format(username=t), reply_markup=kb.confirm_twitter_username)

        return steps.CONFIRM_TWITTER_USERNAME
    else:
        update.message.reply_text(text.twitter_error)
        return steps.GET_TWITTER_USERNAME


def get_email(update: Update, context: CallbackContext):
    '''Get the user's Email'''

    t = update.message.text
    chat_id = update.effective_chat.id

    # ? Validate Email
    if(validators.email(t)):
        db.update(
            'users',
            f"email='{t}'",
            f'id={chat_id}')

        update.message.reply_text(
            text.confirm_email.format(email=t), reply_markup=kb.confirm_email)
        return steps.CONFIRM_EMAIL
    else:
        update.message.reply_text(text.email_error)
        return steps.GET_EMAIL


def edit_email(update: Update, context: CallbackContext):
    '''Edit the user's Email'''

    t = update.message.text
    chat_id = update.effective_chat.id

    # ? Validate Email
    if(validators.email(t)):
        db.update(
            'users',
            f"email='{t}'",
            f'id={chat_id}')

        update.message.reply_text(
            text.edit_done.format(column='Email'))
        account(update, context)
        update.message.reply_text(
            text.home_menu, reply_markup=kb.home)
        return ConversationHandler.END
    else:
        update.message.reply_text(text.edit_email_error)
        return steps.EDIT_EMAIL


def edit_twitter(update: Update, context: CallbackContext):
    '''Edit the user's Twitter'''

    t = update.message.text
    chat_id = update.effective_chat.id

    # ? Username must be at least 4 characters long.
    if(len(t) >= 4 and t.startswith('@') == False):
        db.update(
            'users',
            f"twitter='{t}'",
            f'id={chat_id}')

        update.message.reply_text(
            text.edit_done.format(column='Twitter username'),)
        account(update, context)
        update.message.reply_text(
            text.home_menu, reply_markup=kb.home)
        return ConversationHandler.END
    else:
        update.message.reply_text(text.edit_twitter_error)
        return steps.EDIT_TWITTER


def edit_wallet(update: Update, context: CallbackContext):
    '''Edit the user's Wallet'''

    t = update.message.text
    chat_id = update.effective_chat.id

    # ? Wallet must be started with 0x
    if((config.NETWORK == 'ethereum' and t.startswith('0x') and len(t) >= 42) or (config.NETWORK == 'tron' and t.startswith('T') and len(t) >= 34)):
        db.update(
            'users',
            f"wallet='{t}'",
            f'id={chat_id}')

        update.message.reply_text(
            text.edit_done.format(column='wallet address'),)
        account(update, context)
        update.message.reply_text(
            text.home_menu, reply_markup=kb.home)
        return ConversationHandler.END
    else:
        update.message.reply_text(text.edit_wallet_error)
        return steps.EDIT_WALLET


def get_wallet(update: Update, context: CallbackContext):
    '''Get the user's Wallet'''

    t = update.message.text
    chat_id = update.effective_chat.id

    # ? Wallet must be started with 0x
    if((config.NETWORK == 'ethereum' and t.startswith('0x') and len(t) >= 42) or (config.NETWORK == 'tron' and t.startswith('T') and len(t) >= 34)):
        db.update(
            'users',
            f"wallet='{t}'",
            f'id={chat_id}')

        update.message.reply_text(
            text.confirm_wallet.replace('[WALLET]', t), reply_markup=kb.confirm_wallet)

        return steps.CONFIRM_WALLET
    else:
        update.message.reply_text(text.wallet_error)
        return steps.GET_WALLET


def balance(update: Update, context: CallbackContext):
    '''Send the user's Balance and Referrals'''

    chat_id = update.effective_chat.id
    balance = db.select('balance', 'users', f'id={chat_id}')[0]['balance']
    # referrals = db.get_user_referrals(chat_id)

    if(balance == 0):
        tilde = ''
    else:
        tilde = '~'
    update.message.reply_text(
        text.balance.format(
            tilde=tilde,
            symbol=config.SYMBOL_UPPER,
            units=str(balance),
            balance=str(int(balance*float(config.CURRENT_PRICE))))
    )
    # , referrals=referrals

    # return steps.HOME


def account(update: Update, context: CallbackContext, from_user: int = 0):
    '''Send the user's account information'''

    chat_id = update.effective_chat.id
    user = db.select('*', 'users', f'id={chat_id}')[0]
    referrals, referrals_count = db.get_user_referrals(chat_id)

    # Finally, send the message
    t = text.account.format(
        chat_id=chat_id,
        name=update.effective_chat.first_name,
        email=user['email'], twitter=user['twitter'], referrals_count=referrals_count, referrals=referrals, wallet=user['wallet']).replace('[SYMBOL]', config.SYMBOL_UPPER)

    if(from_user == 0):
        update.message.reply_text(t, reply_markup=kb.edit_information)
    else:
        context.bot.send_message(
            chat_id=from_user, text=t, reply_markup=kb.edit_information)

    # return steps.HOME


def withdraw(update: Update, context: CallbackContext):
    '''Send "withdrawal date" message'''

    setting = db.select('withdraw_status', 'settings')
    if(setting):
        status = setting[0]['withdraw_status']
    else:
        status = db.create_setting()['withdraw_status']

    if(status == 'open'): # or update.effective_chat.id == config.SUDO):
        balance = db.select('balance', 'users',
                            f'id={update.effective_chat.id}')[0]['balance']
        if(balance < int(config.REFERRAL_REWARD)-1):
            update.message.reply_text(text.not_enough_balance)
            return ConversationHandler.END
        else:
            update.message.reply_text(
                text.get_withdraw.replace('[BALANCE]', str(balance)), reply_markup=kb.back)
            return steps.GET_TXID

    else:
        update.message.reply_text(text.withdraw_close,disable_web_page_preview=True)


def referral(update: Update, context: CallbackContext):
    '''Send referral banner of the user'''

    chat_id = update.effective_chat.id

    caption = text.referral_banner.replace(
        "[CHAT_ID]", str(chat_id))
    update.message.reply_photo(photo=open(
        f'files/{config.SYMBOL}.jpg', 'rb'), caption=caption)

    rf, count = db.get_user_referrals(chat_id)

    if(count is 0):
        t = text.your_referrals.format(count=count)
    else:
        t = text.your_referrals_list.format(referrals=rf, count=count)
    update.message.reply_text(t)


def faq(update: Update, context: CallbackContext):
    '''Send FAQ message'''
    update.message.reply_text(text.faq)


def error(update: Update, context: CallbackContext):
    '''Error callback for unknown messages.'''
    update.message.reply_text(text.unknown_error)


def check_join_channel(update: Update, context: CallbackContext):
    '''Check if the user has joined the channels.'''

    # return True
    channel1 = context.bot.get_chat_member(
        chat_id=f'@{config.CHANNEL1}', user_id=update.effective_chat.id)['status']
    # channel2 = context.bot.get_chat_member(
    #     chat_id='@'+config.CHANNEL1, user_id=update.effective_chat.id)['status']

    # Not joined
    L = ['left', 'kicked']
    if(channel1 in L):  # or channel2 in L):
        r = context.bot.send_message(
            chat_id=update.effective_chat.id, text=text.please_wait, reply_markup=kb.hide)
        r.delete()

        update.message.reply_text(
            text.left_from_channel, reply_markup=kb.join_channel)
        return False

    # Joined
    return True
