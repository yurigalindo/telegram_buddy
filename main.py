import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from commands import gpt, defend_stefani, solve_discussion, search_history, summarize_history, ask_history
from utils import save_message

def main():
    # Update logging to only show ERROR level
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    try:
        application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

        application.add_handler(CommandHandler("gpt", gpt))
        application.add_handler(CommandHandler("perguntar_historico", ask_history))
        application.add_handler(CommandHandler("defender_stefani", defend_stefani))
        application.add_handler(CommandHandler("resolver_discussao", solve_discussion))
        application.add_handler(CommandHandler("pesquisar", search_history))
        application.add_handler(CommandHandler("resumir", summarize_history))
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
