import requests
from bs4 import BeautifulSoup as bs
import telebot
from collections import defaultdict


token = '5553017132:AAF8I9gG7Rgb5Gmw4Ml9G7QrNkTBv_w1FYY'
bot = telebot.TeleBot(token)
users = defaultdict(list)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Show coins price")
    btn2 = telebot.types.KeyboardButton("Add coin")
    markup.add(btn1,btn2)
    bot.send_message(message.chat.id, text="Hi".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == "Show coins price":
        costs = []
        names = []
        for i in users[message.chat.id]:
            names.append(get_name(i))
            costs.append(get_cost(i))
        s = ''
        for i, j in zip(costs, names):
            s = s + j+': '+i + '\n'
        bot.send_message(message.chat.id, str('GST: ' + get_cost(URL_TEMPLATE_gst) + '\n' + 'GMT: ' +
        get_cost(URL_TEMPLATE_gmt) + '\n' + 'SOL: ' + get_cost(URL_TEMPLATE_sol) + '\n' + 'USD: ' + get_cost(URL_TEMPLATE_usd) + '\n' + s))
        print(str('GST: ' + get_cost(URL_TEMPLATE_gst) + '\n' + 'GMT: ' +
        get_cost(URL_TEMPLATE_gmt) + '\n' + 'SOL: ' + get_cost(URL_TEMPLATE_sol) + '\n' + 'USD: ' + get_cost(URL_TEMPLATE_usd) + '\n' + s))
    if message.text == 'Add coin':
        bot.send_message(message.chat.id,'Insert URL of coin from coinmarketcap.com')
    if "https://coinmarketcap.com/" in message.text:
        print(message.text)
        users[message.chat.id].append(message.text)


def get_name(url_):
    r = requests.get(url_)
    f = ''
    soup = bs(r.text, features='html.parser')
    name = soup.find(class_='sc-1q9q90x-0 jCInrl h1').get_text()
    print(name)
    return str(name)


def get_cost(url_):
    r = requests.get(url_)
    f = ''
    soup = bs(r.text, features='html.parser')
    cost = soup.find(class_='priceValue').get_text()
    percent = soup.find(class_='sc-15yy2pl-0 feeyND')
    if soup.find(class_='icon-Caret-down'):
        f = '-'
    elif soup.find(class_='icon-Caret-up'):
        f = '+'
    return str(cost + ' (' + f + percent.get_text() + ' 24h)')


URL_TEMPLATE_gst = "https://coinmarketcap.com/currencies/green-satoshi-token/"
URL_TEMPLATE_sol = "https://coinmarketcap.com/currencies/solana/"
URL_TEMPLATE_gmt = "https://coinmarketcap.com/currencies/green-metaverse-token/"
URL_TEMPLATE_usd = "https://coinmarketcap.com/ru/currencies/usd/"


bot.polling(none_stop=True)
