from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔍 Search YouTube", switch_inline_query_current_chat="")]]
)

@Client.on_message(filters.command("help") & filters.private)
async def help(bot, message):
    await message.reply(
        "This bot can search for YouTube videos & download videos, playlists and more.\n\n"
        "◉ Search for videos - <i>Use inline mode</i>\n"
        "◉ Download videos - <i>Send any link of a YouTube video and select a quality</i>\n"
        "◉ Download playlist - <i>Send any link of a YouTube playlist</i>\n"
        "◉ Playlist audio download - <code>/playlist_aud link</code>",
        reply_markup=BUTTONS,
        parse_mode="html"  # ✅ lowercase fixed
    )