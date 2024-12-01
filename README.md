# Telegram GPT Bot

A Telegram bot powered by GPT-4-mini that has fun and helpful functions for a group of friends.

## Prerequisites

- Python 3.12
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- An OpenAI API Key

## Setup

1. Clone the repository

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   OPENAI_API_KEY=your_openai_api_key
   APPROVED_USERS=user_id1,user_id2
   APPROVED_CHATS=chat_id1,chat_id2
   ```

## Running the Bot

1. Activate the virtual environment (if not already activated)
2. Run the bot:
   ```bash
   python main.py
   ```

## Features

The bot supports the following commands:

- `/gpt <message>` - Get a response from GPT-4-mini
- `/defender_stefani` - Defends Stefani's position in recent conversations
- `/resolver_discussao` - Analyzes and helps resolve recent group conflicts
- `/pesquisar <query>` - Search through chat history
- `/resumir` - Summarizes recent chat history

The bot also automatically saves messages for context and history management.

## Security

- Only accepts commands either from the users listed in APPROVED_USERS or from the chats listed in APPROVED_CHATS
- Messages are stored locally in `data/history.txt`
- Chat history is automatically trimmed when it exceeds size limits

## Logging

The bot logs errors to both:
- Console output
- `logs/bot.log` file

Notes:
- Only ERROR level logs are recorded.
- Since it was developed only for one group chat, history from all chats and conversations are stored in the same file.