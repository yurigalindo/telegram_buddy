import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from commands import gpt, save_message, defend_stefani, solve_discussion

def main():
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

    application.add_handler(CommandHandler("gpt", gpt))
    application.add_handler(CommandHandler("defender_stefani", defend_stefani))
    application.add_handler(CommandHandler("resolver_discussao", solve_discussion))
    application.run_polling()

if __name__ == '__main__':
    main()
