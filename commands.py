from dotenv import load_dotenv
from telegram import Update
from utils import check_user, read_history, crop_last_apparition, llm_call, trim_to_context
import logging

logger = logging.getLogger(__name__)

# Load prompts
STEFANI_PROMPT = open('prompts/defend_stefani.txt', 'r').read()
DISCUSSION_PROMPT = open('prompts/solve_discussion.txt', 'r').read()
SEARCH_HISTORY_PROMPT = open('prompts/search_history.txt', 'r').read()
SUMMARIZE_HISTORY_PROMPT = open('prompts/summarize_history.txt', 'r').read()
ASK_HISTORY_PROMPT = open('prompts/ask_history.txt', 'r').read()
load_dotenv()

DEEPSEEK_MODEL = "deepseek/deepseek-v4-flash"


@check_user
async def gpt(update: Update, context):
    response = await llm_call(update.message.text[5:], "You are a helpful assistant.", model=DEEPSEEK_MODEL)
    await update.message.reply_text(response)

@check_user
async def defend_stefani(update: Update, context):
    history = read_history()
    history = trim_to_context(history, DEEPSEEK_MODEL, overhead_chars=len(STEFANI_PROMPT))
    response = await llm_call(history, STEFANI_PROMPT, model=DEEPSEEK_MODEL)
    await update.message.reply_text(response)

@check_user
async def solve_discussion(update: Update, context):
    history = read_history()
    history = trim_to_context(history, DEEPSEEK_MODEL, overhead_chars=len(DISCUSSION_PROMPT))
    response = await llm_call(history, DISCUSSION_PROMPT, model=DEEPSEEK_MODEL)
    await update.message.reply_text(response)

@check_user
async def search_history(update: Update, context):
    what_to_search = " ".join(update.message.text.split(" ")[1:])
    history = read_history()
    history = trim_to_context(history, DEEPSEEK_MODEL, overhead_chars=len(SEARCH_HISTORY_PROMPT) + len(what_to_search) + 100)
    prompt = "You need to search for this: " + what_to_search + "\n This is the chat history: \n" + history
    response = await llm_call(prompt, SEARCH_HISTORY_PROMPT, model=DEEPSEEK_MODEL)
    await update.message.reply_text(response)

@check_user
async def ask_history(update: Update, context):
    message = " ".join(update.message.text.split(" ")[1:])
    history = read_history()
    history = trim_to_context(history, DEEPSEEK_MODEL, overhead_chars=len(ASK_HISTORY_PROMPT) + len(message) + 100)
    prompt = "This is the user message: " + message + "\n This is the chat history: \n" + history
    response = await llm_call(prompt, ASK_HISTORY_PROMPT, model=DEEPSEEK_MODEL)
    await update.message.reply_text(response)

@check_user
async def summarize_history(update: Update, context):
    history = crop_last_apparition(update.message.from_user.username)
    history = trim_to_context(history, DEEPSEEK_MODEL, overhead_chars=len(SUMMARIZE_HISTORY_PROMPT))
    response = await llm_call(history, SUMMARIZE_HISTORY_PROMPT, model=DEEPSEEK_MODEL)
    await update.message.reply_text(response)
