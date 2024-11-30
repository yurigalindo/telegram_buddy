import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI
from utils import parse_message
# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load approved users from environment variable
approved_users = set(os.getenv("APPROVED_USERS").split(','))
approved_users = {int(user) for user in approved_users}

async def handle_message(update: Update, context):
    user_id = update.effective_user.id
    if user_id not in approved_users:
        await update.message.reply_text(f"Unauthorized user. Access denied. Your user is {user_id}")
        return
    
    with open('data/history.txt', 'a') as file:
        file.write(f"{parse_message(update.message)}\n")

def main():
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
