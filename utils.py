import pytz
import os
from dotenv import load_dotenv
from telegram import Update
load_dotenv()

# Load approved users from environment variable
approved_users = set(os.getenv("APPROVED_USERS").split(','))
approved_users = {int(user) for user in approved_users}

def parse_message(message):
    user = message.from_user.username
    text = message.text
    timestamp = message.date.astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y:%m:%d:%H:%M')
    return f"{timestamp} - {user}: {text}"

def check_user(unsecured_function):
    async def secured_function(update: Update, context):
        user_id = update.effective_user.id
        if user_id not in approved_users:
            await update.message.reply_text(f"Unauthorized user. Access denied. Your user is {user_id}")
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