from dotenv import dotenv_values

config = dotenv_values('.env')

bot_token = config['BOT_TOKEN']
exchangerate_token = config['EXCHANGE_TOKEN']
