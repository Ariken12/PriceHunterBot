

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackContext
import logging
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from Core import Core
import structure.Requests as Requests
import structure.Processes as Processes


logging.basicConfig(level=logging.INFO)

def main():
    core = Core()
    bot = ApplicationBuilder().token(os.environ.get('API_KEY')).build()
    
    for repeater in Processes.__all__:
        repeater = Processes.__dict__[repeater](core)
        bot.job_queue.run_repeating(repeater, interval=repeater.interval, first=repeater.start_delay)
    
    for request in Requests.__all__:
        bot.add_handler(Requests.__dict__[request](core))

    try:
        bot.run_polling()
    except Exception as e:
        logging.error(f'{type(e)}: {e}')
        core.dump()

if __name__ == '__main__':
    main()