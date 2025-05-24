from dotenv import load_dotenv
from telegram import Update
from utils import check_user, read_history, crop_last_apparition, gpt_call
import logging

logger = logging.getLogger(__name__)

# Load prompts
STEFANI_PROMPT = open('prompts/defend_stefani.txt', 'r').read()
DISCUSSION_PROMPT = open('prompts/solve_discussion.txt', 'r').read()
SEARCH_HISTORY_PROMPT = open('prompts/search_history.txt', 'r').read()
SUMMARIZE_HISTORY_PROMPT = open('prompts/summarize_history.txt', 'r').read()
ASK_HISTORY_PROMPT = open('prompts/ask_history.txt', 'r').read()
load_dotenv()


@check_user
async def gpt(update: Update, context):
    response = await gpt_call(update.message.text[5:], "You are a helpful assistant.")
    await update.message.reply_text(f"GPT says:\n{response}")

@check_user
async def defend_stefani(update: Update, context):
    history = read_history(limit=400)
    response = await gpt_call(history, STEFANI_PROMPT)
    await update.message.reply_text(response)

@check_user
async def solve_discussion(update: Update, context):
    history = read_history()
    response = await gpt_call(history, DISCUSSION_PROMPT)
    await update.message.reply_text(response)

@check_user
async def search_history(update: Update, context):
    history = read_history()
    what_to_search = " ".join(update.message.text.split(" ")[1:]) # ignore the command
    prompt = "You need to search for this: " + what_to_search + "\n This is the chat history: \n" + history
    response = await gpt_call(prompt, SEARCH_HISTORY_PROMPT)
    await update.message.reply_text(response)

@check_user
async def ask_history(update: Update, context):
    history = read_history()
    message = " ".join(update.message.text.split(" ")[1:]) # ignore the command
    prompt = "This is the user message: " + message + "\n This is the chat history: \n" + history
    response = await gpt_call(prompt, ASK_HISTORY_PROMPT)
    await update.message.reply_text(response)

@check_user
async def summarize_history(update: Update, context):
    history = crop_last_apparition(update.message.from_user.username)
    response = await gpt_call(history, SUMMARIZE_HISTORY_PROMPT)
    await update.message.reply_text(response)
