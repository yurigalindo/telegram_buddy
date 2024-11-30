import pytz
import os
from dotenv import load_dotenv
from telegram import Update
load_dotenv(override=True)

# Load approved users from environment variable
approved_users = set(os.getenv("APPROVED_USERS").split(','))
approved_users = {int(user) for user in approved_users}
approved_chats = set(os.getenv("APPROVED_CHATS").split(','))
approved_chats = {int(chat) for chat in approved_chats}

def parse_message(message):
    if not message:
        return "Unknown message"
    
    user = (message.from_user.username 
            if message.from_user and message.from_user.username 
            else message.from_user.first_name if message.from_user  and message.from_user.first_name
            else "Unknown user")
    
    text = message.text if message.text else "No text"


    timestamp = message.date.astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y:%m:%d:%H:%M') if message.date else "Unknown timestamp"

    return f"{timestamp} - {user}: {text}"

def check_user(unsecured_function):
    async def secured_function(update: Update, context):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        if user_id not in approved_users and chat_id not in approved_chats:
            await update.message.reply_text(f"Unauthorized user. Access denied.")
            return
        return await unsecured_function(update, context)
    return secured_function

def read_history(limit: int | None = None):
    with open('data/history.txt', 'r') as file:
        full_history = file.read()
    if limit:
        lines = full_history.splitlines()
        return '\n'.join(lines[-limit:])
    return full_history