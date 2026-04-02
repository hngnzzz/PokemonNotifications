# Discord Pokemon Bot

## Setup

1. Create the local virtual environment:
   `py -m venv .venv`
2. Activate it:
   `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   `py -m pip install -r requirements.txt`
4. Copy `.env.example` to `.env`.
5. Put your Discord bot token into `.env`.
6. Optional: set `DISCORD_GUILD_ID` for faster slash-command sync in one server.
7. Run:
   `py bot.py`

## Discord setup

- Enable `MESSAGE CONTENT INTENT` in the Discord Developer Portal because the bot reads message content in `on_message`.
- Invite the bot with both `bot` and `applications.commands` scopes.
- Make sure the bot has permission to view channels, read message history, and send messages in the target server.

## Test command

Send `!ping` in a server where the bot is present.
