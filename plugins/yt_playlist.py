import os
from pytube import Playlist
from pyrogram import Client, filters
from pyrogram.errors import MessageIdInvalid

if not os.path.exists("downloads"):
    os.makedirs("downloads")

PLAYLIST_REGEX = r'(.*)youtube.com/(.*)[&|?]list=(?P<playlist>[^&]*)(.*)'

@Client.on_message(filters.command("playlist_aud"))
async def playlist_audio(bot, message):
    link = message.text[12:].strip()
    chat_id = message.chat.id

    try:
        playlist = Playlist(link)
    except Exception as e:
        return await message.reply_text(f"❌ Invalid playlist link or error:\n<code>{e}</code>")

    total = len(playlist.videos)
    count = 0

    msg = await message.reply_text(f"🎧 Downloading playlist (Audio)\n\n✅ {count}/{total} completed")

    for video in playlist.videos:
        try:
            file_path = video.streams.get_audio_only().download(output_path="downloads")
            await bot.send_audio(chat_id, audio=file_path, caption=video.title + ".mp3",
                                 file_name=video.title + ".mp3", duration=video.length,
                                 performer=video.author)
            os.remove(file_path)
            count += 1
            await msg.edit_text(f"🎧 Downloading...\n✅ {count}/{total} completed")
        except Exception as e:
            await bot.send_message(chat_id, f"⚠️ Error:\n<code>{e}</code>")

    await msg.edit_text(f"✅ Playlist downloaded successfully (Audio)\n\n{count}/{total} done!")

@Client.on_message(filters.regex(PLAYLIST_REGEX))
async def playlist_video(bot, message):
    link = message.text.strip()
    chat_id = message.chat.id

    try:
        playlist = Playlist(link)
    except Exception as e:
        return await message.reply_text(f"❌ Invalid playlist link or error:\n<code>{e}</code>")

    total = len(playlist.videos)
    count = 0

    msg = await message.reply_text(f"📥 Downloading playlist (Video)\n\n✅ {count}/{total} completed")

    for video in playlist.videos:
        try:
            stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
            if not stream:
                await bot.send_message(chat_id, f"⚠️ Skipped: No video stream found for '{video.title}'")
                continue

            file_path = stream.download(output_path="downloads")
            await bot.send_video(chat_id, video=file_path, caption=video.title)
            os.remove(file_path)
            count += 1
            await msg.edit_text(f"📥 Downloading...\n✅ {count}/{total} completed")
        except Exception as e:
            await bot.send_message(chat_id, f"⚠️ Error:\n<code>{e}</code>")

    await msg.edit_text(f"✅ Playlist downloaded successfully (Video)\n\n{count}/{total} done!")