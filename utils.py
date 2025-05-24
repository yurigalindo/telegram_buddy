import pytz
import os
from dotenv import load_dotenv
from telegram import Update
import logging
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)

MAX_CHARS = 360_000  # less than 128k tokens
HISTORY_FILE = 'data/history.txt'


# Load approved users from environment variable
approved_users = set(os.getenv("APPROVED_USERS").split(','))
approved_users = {int(user) for user in approved_users}
approved_chats = set(os.getenv("APPROVED_CHATS").split(','))
approved_chats = {int(chat) for chat in approved_chats}


async def gpt_call(message: str, system_prompt: str, model: str = "gpt-4o-mini"):
    try:
        messages=[
            {"role": "system", "content": system_prompt},
        ]
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling GPT: {e}", exc_info=True)
        return "I'm sorry, I'm having trouble connecting to GPT."
    
def check_user(unsecured_function):
    async def secured_function(update: Update, context):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        if user_id not in approved_users and chat_id not in approved_chats:
            await update.message.reply_text(f"Unauthorized user. Access denied.")
            return
        return await unsecured_function(update, context)
    return secured_function

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

@check_user
async def save_message(update: Update, context):
    try:
        with open(HISTORY_FILE, 'a') as file:
            file.write(f"{parse_message(update.message)}\n")
    except Exception as e:
        logger.error(f"Error managing message history: {e}", exc_info=True)

def read_history(limit: int | None = None):
    try:
        with open(HISTORY_FILE, 'r') as file:
            content = file.read()
            
        # Trim file if it exceeds max_chars
        # This is a bit IO intensive, but the file isn't that big and this function only runs ocasionally
        if len(content) > MAX_CHARS:
            excess_chars = len(content) - MAX_CHARS
            lines = content.splitlines(True) # Keep newline characters
            
            chars_to_remove_count = 0
            lines_to_remove_count = 0
            
            for line in lines:
                if chars_to_remove_count >= excess_chars:
                    break
                chars_to_remove_count += len(line)
                lines_to_remove_count += 1
            lines_to_remove_count += 50 # remove some extra buffer so that it doesn't run again if called on a short interval
            
            keep_lines = lines[lines_to_remove_count:]
            
            # Write back the trimmed content
            with open(HISTORY_FILE, 'w') as f:
                content = ''.join(keep_lines)
                f.write(content)
        
        if limit:
            lines = content.splitlines()
            return '\n'.join(lines[-limit:])
        return content

    except Exception as e:
        logger.error(f"Error reading history file: {e}", exc_info=True)
        return ""
    
def crop_last_apparition(username: str):
    """
    Returns all messages that appear after the last message from the specified username.
    If username is not found, returns whole history.
    """
    history = read_history()
    lines = history.splitlines()
    last_contiguous = True # if the last messages come from the username, disregard them
    for i, line in enumerate(reversed(lines)):
        try:
            if username in line.split(" - ")[1].split(":")[0]:
                if last_contiguous:
                    continue
                return "".join(lines[-i:])
            else:
                last_contiguous = False
        except Exception as e:
            continue
    return history