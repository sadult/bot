import os
import subprocess
from strings import kb, steps, text
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from handlers import db, message
import importlib
import sys

config = importlib.import_module('configs.'+sys.argv[0].split('.')[0])


def start(update: Update, context: CallbackContext):
    '''Start of the bot'''

    # Get full name of user
    full_name = update.effective_chat.first_name
    if(update.effective_chat.last_name):
        full_name = full_name+' '+update.effective_chat.last_name

    # if /start has referred_by parameter
    if(context.args and db.select('id', 'users', f'id={context.args[0]}') != None):

        # if user click on his own referral link
        if(int(context.args[0]) == update.effective_chat.id):
            update.message.reply_text(text.self_referral)
            referred_by = None
        else:
            referred_by = context.args[0]
    else:
        referred_by = None

    # ? Insert user in DB if not exist and get current status
    status = db.create_user(chat_id=update.effective_chat.id,
                            name=full_name, referred_by=referred_by)['status']

    # ? If the user has not yet completed all his tasks.
    if(status == 'registering'):

        # Send a temporary message, then delete it to hide the keyboard
        r = context.bot.send_message(
            chat_id=update.effective_chat.id, text=text.please_wait, reply_markup=kb.hide)
        r.delete()

        # Send start registering banner
        t = text.start_registering.replace("[NAME]",
                                           update.effective_chat.first_name)
        update.message.reply_text(text=t, reply_markup=kb.kb_continue)
        # update.message.reply_photo(photo=open(
        #     'files/start_banner.jpg', 'rb'), caption=caption, reply_markup=kb.kb_continue)

        return steps.START_REGISTERING

    # ? If the user has already completed all his tasks.
    elif(status == 'active'):

        # Send home menu message
        joined = message.check_join_channel(update, context)
        if(joined):
            update.message.reply_text(
                text=text.start.replace('[NAME]', update.effective_chat.first_name), reply_markup=kb.home)

        return ConversationHandler.END


def commands(update: Update, context: CallbackContext):
    '''Help command for Sudo (not planned yet)'''
    commands = "🎛 <b>Sudo Commands:</b>\n\n"
    for handler in context._dispatcher.handlers[0]:
        if(handler.__class__ != ConversationHandler):
            name = handler.callback.__name__
            if(name not in ['start', 'handler']):
                commands += '/'+name + '\n'
    update.message.reply_text(commands)


def withdraw(update: Update, context: CallbackContext):
    '''Change withdrawal status of the bot (ONLY FOR SUDO!)'''

    # if command has parameters
    if(context.args and context.args[0] in ['open', 'close']):
        new_status = context.args[0]
        db.update('settings', f"withdraw_status='{new_status}'")
        update.message.reply_text(
            f'✅ Withdrawal status changed to <b>{context.args[0]}.</b>')
    else:
        update.message.reply_text('❌ Example: /withdraw open|close')


def users(update: Update, context: CallbackContext):
    '''Send users of the bot (ONLY FOR SUDO!)'''

    users = db.select('*', 'users')

    for user in users:
        t = f"👤 <b>{user['name']}</b>\n\n"
        for val in user:
            t += (f"🔹 <b>{val} :</b> {user[val]}\n")
        update.message.reply_text(t)


def stats(update: Update, context: CallbackContext):
    '''Statistics of the bot (ONLY FOR SUDO!)'''

    total_count = db.select(
        'count(id) as count', 'users')[0]['count']
    registering_count = db.select(
        'count(id) as count', 'users', "status='registering'")[0]['count']
    actives_count = db.select(
        'count(id) as count', 'users', "status='active'")[0]['count']

    result = f'''
👥 <b>Total users : </b>{total_count}

🟡 <b>Not registered users : </b>{registering_count}
🟢 <b>Registered users : </b>{actives_count}
    '''
    update.message.reply_text(result)


def delete_db(update: Update, context: CallbackContext):
    '''Delete database of the bot (ONLY FOR SUDO!)'''

    cmd = f'rm databases/{config.SYMBOL}.db'
    update.message.reply_text(run_command(cmd.split()))
    update.message.reply_text("✅ <b>Database deleted successfully.</b>")


def send_to_all(update: Update, context: CallbackContext):
    '''Send message to all users (ONLY FOR SUDO!)'''
    update.message.reply_text(
        "📝 <b>Send your S2A message (to all users):</b>", reply_markup=kb.backtohome)

    return steps.GET_S2A_ALL

def send_to_not_registered(update: Update, context: CallbackContext):
    '''Send message to Not registered users (ONLY FOR SUDO!)'''
    update.message.reply_text(
        "📝 <b>Send your S2A message (to not registered users):</b>", reply_markup=kb.backtohome)

    return steps.GET_S2A_NR

def send_to_registered(update: Update, context: CallbackContext):
    '''Send message to registered users (ONLY FOR SUDO!)'''
    update.message.reply_text(
        "📝 <b>Send your S2A message (to registered users):</b>", reply_markup=kb.backtohome)

    return steps.GET_S2A_R


def sql(update: Update, context: CallbackContext):
    '''Run SQL Command (ONLY FOR SUDO!)'''

    sql = ' '.join(context.args)
    update.message.reply_text(
        '♻️ <b>Executing SQL:</b>\n\n'+sql)
    update.message.reply_text('⚙️ <b>Result of SQL :</b>\n\n'+str(db.sql(sql)))


def shell(update: Update, context: CallbackContext):
    '''Run Shell Command (ONLY FOR SUDO!)'''

    cmd = ' '.join(context.args)
    update.message.reply_text(
        '♻️ <b>Executing Command:</b>\n\n'+cmd)
    update.message.reply_text(run_command(cmd))


def restart(update: Update, context: CallbackContext):
    '''Restart the bot (ONLY FOR SUDO!)'''
    update.message.reply_text(
        "♻️ <i>Bot is going to restart in few seconds.</i>\n\n⚠️ <b>You need to /start again, bot does'nt remind you when restarted!</b>")

    pid = os.getpid()
    cmd = f'sh restart.sh {pid} {config.SYMBOL}'
    update.message.reply_text(run_command(cmd.split()))


def run_command(cmd):
    '''Run shell commands and returns output of terminal'''
    output = subprocess.run(
        cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    if(output):
        return "⚙️ <b>Result of terminal :</b>\n\n" + str(output)
    else:
        return "✅ <b>This command had no output but was executed without any error.</b>"


def error(update: Update, context: CallbackContext):
    '''Error callback for unknown commands.'''
    update.message.reply_text(text.unknown_command)
