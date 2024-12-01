import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from utils import parse_message, check_user, read_history, crop_last_apparition
import logging

logger = logging.getLogger(__name__)

# Load prompts
STEFANI_PROMPT = open('prompts/defend_stefani.txt', 'r').read()
DISCUSSION_PROMPT = open('prompts/solve_discussion.txt', 'r').read()
SEARCH_HISTORY_PROMPT = open('prompts/search_history.txt', 'r').read()
SUMMARIZE_HISTORY_PROMPT = open('prompts/summarize_history.txt', 'r').read()
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@check_user
async def save_message(update: Update, context):
    try:
        history_file = 'data/history.txt'
        # Add new message
        with open(history_file, 'a') as file:
            file.write(f"{parse_message(update.message)}\n")
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

@check_user
async def search_history(update: Update, context):
    history = read_history()
    what_to_search = " ".join(update.message.text.split(" ")[1:]) # ignore the command
    prompt = "You need to search for this: " + what_to_search + "\n This is the chat history: \n" + history
    response = await _gpt_call(prompt, SEARCH_HISTORY_PROMPT)
    await update.message.reply_text(response)

@check_user
async def summarize_history(update: Update, context):
    history = crop_last_apparition(update.message.from_user.username)
    response = await _gpt_call(history, SUMMARIZE_HISTORY_PROMPT)
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
