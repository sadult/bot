from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup)
from telegram.replykeyboardremove import ReplyKeyboardRemove
from strings import btn
import sys
import importlib

config = importlib.import_module('configs.'+sys.argv[0].split('.')[0])


hide = ReplyKeyboardRemove()

# Select information to edit
select_information = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.edit_email, callback_data='edit_email')
    ],
    [
        InlineKeyboardButton(text=btn.edit_twitter,
                             callback_data='edit_twitter')
    ],
    [
        InlineKeyboardButton(text=btn.edit_wallet, callback_data='edit_wallet')
    ],
    [
        InlineKeyboardButton(text=btn.back, callback_data='back_account')
    ],
], resize_keyboard=True)

# Edit information
edit_information = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.edit_information,
                             callback_data='edit_information'),
    ],
], resize_keyboard=True)

# Back to select information menu
back_select = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.back, callback_data='back_select'),
    ],
], resize_keyboard=True)

# Back to home menu
back = ReplyKeyboardMarkup([
    [
        KeyboardButton(btn.back),
    ],
], resize_keyboard=True)

# Back to home menu
backtohome = ReplyKeyboardMarkup([
    [
        KeyboardButton(btn.backtohome),
    ],
], resize_keyboard=True)

# Home menu
home = ReplyKeyboardMarkup([
    [
        KeyboardButton(btn.withdraw),
    ],
    [
        KeyboardButton(btn.referral),
        KeyboardButton(btn.balance),
    ],
    [
        KeyboardButton(btn.account),
        KeyboardButton(btn.faq),
    ]
], resize_keyboard=True)

# Continue button below the start banner
kb_continue = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.btn_continue, callback_data='continue')
    ]
])

# Join Channel buttons + Done button
join_channel_with_done = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.join_channel1,
                             url=f'https://t.me/{config.CHANNEL1}')
    ],
    # [
    #     InlineKeyboardButton(text=btn.join_channel2,
    #                          url=f'https://t.me/{config.CHANNEL2}')
    # ],
    [
        InlineKeyboardButton(text=btn.done, callback_data='check_join_channel')
    ]
])

# Only "join channel" buttons
join_channel = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.join_channel1,
                             url=f'https://t.me/{config.CHANNEL1}')
    ]
    # [
    #     InlineKeyboardButton(text=btn.join_channel2,
    #                          url=f'https://t.me/{config.CHANNEL2}')
    # ],
])

# Follow Twitter button + Done button
follow_twitter = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.follow_twitter,
                             url=f'https://twitter.com/{config.TWITTER}')],
    [
        InlineKeyboardButton(
            text=btn.done, callback_data='follow_twitter_done')
    ]
])

# Confirm twitter username
confirm_twitter_username = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text=btn.confirm, callback_data='confirm_twitter_username')
    ]
])

# Confirm Email
confirm_email = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.confirm, callback_data='confirm_email')
    ]
])

# Confirm wallet
confirm_wallet = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.confirm, callback_data='confirm_wallet')
    ]
])

# Withdraw Done
withdraw_done = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=btn.done, callback_data='withdraw_done')
    ]
])
