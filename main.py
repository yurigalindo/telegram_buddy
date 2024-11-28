import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI

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
    
    user_message = update.message.text
    
    # Generate response using GPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    
    bot_response = response.choices[0].message.content
    await update.message.reply_text(bot_response)

def main():
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
