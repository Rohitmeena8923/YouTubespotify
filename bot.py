import threading
from pyrogram import Client
from config import Config
from server import app  # Flask app import

# Start Flask server in background
def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

# Pyrogram bot start
plugins = dict(root="plugins")

print("Bot is running!")

bot = Client(
    "bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=plugins
)
bot.run()