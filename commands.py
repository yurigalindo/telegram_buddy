import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from utils import parse_message, check_user, read_history
import logging

logger = logging.getLogger(__name__)

# Load prompts
STEFANI_PROMPT = open('prompts/defend_stefani.txt', 'r').read()
DISCUSSION_PROMPT = open('prompts/solve_discussion.txt', 'r').read()
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@check_user
async def save_message(update: Update, context):
    try:
        max_chars = 450_000  # less than 128k tokens
        history_file = 'data/history.txt'
        
        # Add new message
        with open(history_file, 'a') as file:
            file.write(f"{parse_message(update.message)}\n")
        
        # Check file size and trim if necessary
        with open(history_file, 'r') as file:
            content = file.read()
            if len(content) > max_chars:
                # Keep the last 75% of the content
                lines = content.splitlines()
                keep_lines = lines[len(lines)//4:]  # Remove first 25% of lines
                
                # Write back the trimmed content
                with open(history_file, 'w') as f:
                    f.write('\n'.join(keep_lines) + '\n')
                    
    except Exception as e:
        logger.error(f"Error managing message history: {e}", exc_info=True)

@check_user
async def gpt(update: Update, context):
    response = await _gpt_call(update.message.text[5:], "You are a helpful assistant.")
    await update.message.reply_text(f"GPT says:\n{response}")

@check_user
async def defend_stefani(update: Update, context):
    history = read_history()
    response = await _gpt_call(history, STEFANI_PROMPT)
    await update.message.reply_text(response)

@check_user
async def solve_discussion(update: Update, context):
    history = read_history()
    response = await _gpt_call(history, DISCUSSION_PROMPT)
    await update.message.reply_text(response)

async def _gpt_call(message: str, system_prompt: str):
    try:
        messages=[
            {"role": "system", "content": system_prompt},
        ]
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling GPT: {e}", exc_info=True)
        return "I'm sorry, I'm having trouble connecting to GPT."
