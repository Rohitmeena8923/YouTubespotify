from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔍 Search YouTube", switch_inline_query_current_chat="")]]
)

@Client.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    await message.reply(
        f"Hello {message.from_user.first_name}! 👋\n\n"
        "This bot can search and download YouTube videos and playlists.\n"
        "Use /help to learn how to use the bot.",
        reply_markup=START_BUTTONS,
        parse_mode="html"
    )