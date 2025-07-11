import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from youtubesearchpython import VideosSearch
from pytube import YouTube

if not os.path.exists("downloads"):
    os.makedirs("downloads")

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔍Search YouTube", switch_inline_query_current_chat="")]
])

yt_link = None
chat_id = None
link = None

@Client.on_inline_query()
async def inlinequery(client, inline_query):
    global yt_link
    query = inline_query.query.strip()
    answer = []

    if query == "":
        return await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Search any YouTube video...",
                    input_message_content=InputTextMessageContent("Search Youtube Videos..."),
                    description="Type to search!",
                    reply_markup=START_BUTTONS
                )
            ],
            cache_time=1
        )

    search = VideosSearch(query, limit=10).result()
    for item in search["result"]:
        yt_link = item["link"]
        answer.append(
            InlineQueryResultArticle(
                title=item["title"],
                thumb_url=item["thumbnails"][0]["url"],
                description=item["viewCount"]["short"],
                input_message_content=InputTextMessageContent(
                    f"📝**Title:** {item['title']}\n"
                    f"👁️‍🗨️**Views:** {item['viewCount']['short']}\n"
                    f"⌛**Duration:** {item['duration']}\n"
                    f"📅**Published:** {item['publishedTime']}\n"
                    f"📢**Channel:** {item['channel']['name']}\n"
                    f"📽️**Watch Video:** <a href='{item['link']}'>Click here</a>"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🎥Watch on YouTube", url=item["link"]),
                        InlineKeyboardButton("🔍Search again", switch_inline_query_current_chat="")
                    ],
                    [InlineKeyboardButton("📁Download", callback_data="link_down")]
                ])
            )
        )

    await inline_query.answer(results=answer, cache_time=1)

yt_regex = r'(.*)youtube.com/(.*)[&|?]v=(?P<video>[^&]*)(.*)'

QUALITY_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📽️High Quality", callback_data="highest_res"),
     InlineKeyboardButton("📽️720p", callback_data="720p")],
    [InlineKeyboardButton("📽️Low Quality", callback_data="lowest_res"),
     InlineKeyboardButton("📽️480p", callback_data="480p")],
    [InlineKeyboardButton("🎵Audio", callback_data="audio"),
     InlineKeyboardButton("📽️360p", callback_data="360p")]
])

@Client.on_message(filters.regex(yt_regex))
async def yt_download(client, message):
    global chat_id, link
    chat_id = message.chat.id
    link = message.text
    dur = VideosSearch(link, limit=1).result()
    _duration = dur["result"][0]["duration"]
    await message.reply_text(f"Select your preferred format\n\nDuration: {str(_duration)}", reply_markup=QUALITY_BUTTONS)

@Client.on_callback_query()
async def callback_query(client, callback):
    try:
        youtube = YouTube(link)
    except Exception as e:
        return await callback.message.edit_text(f"❌ Invalid YouTube link or error: {e}")

    await callback.message.edit_text("📥 Downloading... Please wait.")

    try:
        if callback.data == "highest_res":
            stream = youtube.streams.get_highest_resolution()
        elif callback.data == "lowest_res":
            stream = youtube.streams.get_lowest_resolution()
        elif callback.data == "audio":
            stream = youtube.streams.get_audio_only()
        elif callback.data == "720p":
            stream = youtube.streams.get_by_resolution("720p")
        elif callback.data == "360p":
            stream = youtube.streams.get_by_resolution("360p")
        elif callback.data == "480p":
            stream = youtube.streams.get_by_resolution("480p")
        elif callback.data == "link_down":
            return await callback.message.edit_text(
                f"📎 Video link: `{yt_link}`\n\nCopy this link and send it again to choose download quality."
            )
        else:
            return await callback.message.edit_text("❌ Unknown quality option.")

        file_path = stream.download(output_path="downloads")

        if callback.data == "audio":
            await client.send_audio(chat_id, file_path, caption=youtube.title, performer=youtube.author, duration=youtube.length)
        else:
            await client.send_video(chat_id, file_path, caption=youtube.title)

        os.remove(file_path)
        await callback.message.delete()

    except Exception as error:
        await client.send_message(chat_id, f"⚠️ Error occurred:\n<code>{error}</code>")