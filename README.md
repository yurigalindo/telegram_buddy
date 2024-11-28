# Telegram GPT Bot

A simple Telegram bot powered by OpenAI's GPT-3.5 that responds to messages.

## Prerequisites

- Python 3.7+
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
   ```

## Running the Bot

1. Activate the virtual environment (if not already activated)
2. Run the bot:
   ```bash
   python main.py
   ```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to begin
3. Send any message to get a response from GPT

Note: Only users with IDs listed in APPROVED_USERS will be able to interact with the bot.