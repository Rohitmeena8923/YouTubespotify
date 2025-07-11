from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔍Search YouTube", switch_inline_query_current_chat="")
        ]
    ]
)

@Client.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    reply_markup = START_BUTTONS
    await message.reply(
        f"Hello {message.from_user.first_name}!\n\n"
        "This bot can search for YouTube videos & download YouTube videos, playlists and more. "
        "To search videos click the below \"🔍Search Youtube\" button.\n\n"
        "● /playlist_aud - <i>link</i> :- To download playlist videos in audio format\n"
        "● /help :- For more info.",
        reply_markup=reply_markup,
        parse_mode="html"
    )