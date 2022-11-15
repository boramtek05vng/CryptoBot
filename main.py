import os
import telebot
from telebot import types 
from numerize import numerize as nr
import requests 
import text
#Start the bot
API_KEY = os.environ['API']
bot = telebot.TeleBot(API_KEY)

id = "ethereum"

result = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+id+"&order=market_cap_desc").json()[0]
print(type(nr.numerize(result['market_cap'],3)))
print(result['current_price'])
    

      
def button_gen(buttons):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    for x in buttons:
        markup.add(types.KeyboardButton(x)) 
    return markup

#/start command
@bot.message_handler(commands=['start'])
def send_hello(message):
    #Init keyboard markup
    #Add to buttons by list with ours generate_buttons function.
    markup = button_gen(['CryptoCheck','Prediction'])
    message = bot.send_message(message.chat.id, "Please choose an option:",reply_markup=markup)
    #Here we assign the next handler function and pass in our response from the user. 
    bot.register_next_step_handler(message, ask_options)

#Here we no longer need to specify the decorator function
def ask_options(message):
    if message.text in ['CryptoCheck']:
        message = bot.send_message(message.chat.id, text.enter_coin_msg)
        bot.register_next_step_handler(message, info_check)
    elif message.text in ['Prediction']: 
        message = bot.send_message(message.chat.id,"Coming Soon...")

  
  
def info_check(message):
    try:  
        #Analyze string then return value
        result = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+message.text.lower()+"&order=market_cap_desc").json()[0]
        message = bot.send_message(message.chat.id,
        "Name: " + result['name'] + "\n")
        """Price: " + str(result['current_price']) + " USD" + "\n" + 
        "Market cap: " + result['market_cap']+ " USD" + "\n" + 
        "Market cap rank: " + result['market_cap_rank'] + "\n" + 
        "Total volume: " + nr.numerize(result['name'],3) +" USD"+ "\n" + 
        "High (24h): " + result['high_24h'] + "\n" + 
        "Low (24h): " + result['low_24h'] + "\n" + 
        "Price change (24h): " + result['price_change_24h'] + "\n" + 
        "Price change % (24h): " + result['price_change_percentage_24h'] + "\n" + 
        "Market cap change (24h): " + result['market_cap_change_24h'] + "\n" + 
        "Market cap change % (24h): " + result['market_cap_change_percentage_24h'] + "\n" + 
        "Circulating supply: " + result['circulating_supply'] + "\n" + 
        "Total supply: " + result['total_supply'] + "\n" + 
        "ATH (All time high): " + result['ath'] + "\n" + 
        "ATL (All time low): " + result['atl'] + "\n")"""
        
        #Add to buttons by list with ours generate_buttons function.
        markup = button_gen(['CryptoCheck','Prediction'])
        message = bot.send_message(message.chat.id, "Please choose what to do next:",reply_markup=markup) 
        bot.register_next_step_handler(message, ask_options)
    except Exception:
        message = bot.send_message(message.chat.id,text.invalid_symbol_msg)
        bot.register_next_step_handler(message, info_check) 
      
bot.infinity_polling()