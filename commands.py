import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from utils import parse_message, check_user, read_history

# Load prompts
STEFANI_PROMPT = open('prompts/defend_stefani.txt', 'r').read()

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@check_user
async def save_message(update: Update, context):
    with open('data/history.txt', 'a') as file:
        file.write(f"{parse_message(update.message)}\n")

@check_user
async def gpt(update: Update, context):
    response = await _gpt_call(update.message.text[5:], "You are a helpful assistant.")
    await update.message.reply_text(f"GPT says:\n{response}")

@check_user
async def defend_stefani(update: Update, context):
    if len(update.message.text) > len("defender_stefani") + 2:
        history = read_history(limit=int(update.message.text[len("defender_stefani") + 2:]))
    else:
        history = read_history()
    response = await _gpt_call(history, STEFANI_PROMPT)
    await update.message.reply_text(response)

async def _gpt_call(message: str, system_prompt: str):
    messages=[
            {"role": "system", "content": system_prompt},
        ]
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content