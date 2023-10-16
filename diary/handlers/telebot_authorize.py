from services.user import User
from templates import render_template
from selenium_parser.BasePages import SearchHelper
import telebot
from config import TOKEN
import threading
import asyncio 
import time

bot = telebot.TeleBot(TOKEN)

def test():
    while True:
        bot.send_message(chat_id=1122659029,
                         text="test")
        time.sleep(5)

def main():
    thread = threading.Thread(target=test)
    thread.start()
