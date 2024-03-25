#https://t.me/scrapp7bot
import requests
from bs4 import BeautifulSoup
import telebot
import time

BOT_TOKEN = ''
CHAT_ID = ''
URL = 'https://borkena.com/'

bot = telebot.TeleBot(BOT_TOKEN)
scraping_active = False 


@bot.message_handler(commands=['stop'])
def handle_stop_command(message):
    global scraping_active
    if scraping_active:
        scraping_active = False
        bot.send_message(message.chat.id, "headline scraping stopped")
    else:
        bot.send_message(message.chat.id, "no scraping is currently active")
@bot.message_handler(commands=['start'])
def handle_scrape_command(message):
    global scraping_active
    if scraping_active:
        bot.send_message(message.chat.id, "already scraping headlines")
    else:
        scraping_active = True
        bot.send_message(message.chat.id, "starting to fetch and send headlines...")
    while scraping_active:
            scrape_and_send_headlines()
            time.sleep(60 * 50000)  
def scrape_and_send_headlines():
  try:
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('h3')
    formatted_headlines = []
    for headline in headlines:
      text = headline.text.strip()
      formatted_headlines.append(f"- {text}\n")

    for headline in formatted_headlines:
      bot.send_message(CHAT_ID, headline, parse_mode='Markdown')

  except requests.exceptions.RequestException as e:
    bot.send_message(CHAT_ID, f"Error fetching webpage: {e}")
bot.polling()
