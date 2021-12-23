import os
import urllib
from .commands import encode_string
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *


#### FOR PRIVATE ####


@Client.on_message((filters.document|filters.video|filters.audio|filters.photo) & filters.incoming & ~filters.edited & ~filters.channel)
async def storefile(c, m):
    if IS_PRIVATE:
        if m.from_user.id not in AUTH_USERS:
            return
    send_message = await m.reply_text("**Processing...**", quote=True)
    media = m.document or m.video or m.audio or m.photo
    # text
    text = ""
    if not m.photo:
        text = "--**🗃️ Fɪʟᴇ Dᴇᴛᴀɪʟs:**--\n\n"
        text += f"📂 ** Fɪʟᴇ ɴᴀᴍᴇ :** `{media.file_name}`\n\n" if media.file_name else ""
        text += f"🍃 **Mɪᴍᴇ Tʏᴘᴇ:** __{media.mime_type}__\n\n" if media.mime_type else ""
        text += f"📦 **Fɪʟᴇ ꜱɪᴢᴇ :** __{humanbytes(media.file_size)}__\n\n" if media.file_size else ""
        if not m.document:
            text += f"🎞 **Dᴜʀᴀᴛɪᴏɴ:** __{TimeFormatter(media.duration * 1000)}__\n\n" if media.duration else ""
            if m.audio:
                text += f"🎵 **Tɪᴛʟᴇ:** __{media.title}__\n\n" if media.title else ""
                text += f"🎙 **Pᴇʀғᴏʀᴍᴇʀ:** __{media.performer}__\n\n" if media.performer else ""
    text += f"**✏ Cᴀᴘᴛɪᴏɴ:** __{m.caption}__\n\n" if m.caption else ""
    text += f"**🍁--Uᴘʟᴏᴀᴅᴇᴅ Bʏ :--** [{m.from_user.first_name}](tg://user?id={m.from_user.id}) \n\n"
        

    
    # if databacase channel exist forwarding message to channel
    if DB_CHANNEL_ID:
        msg = await m.copy(int(DB_CHANNEL_ID))
        await msg.reply(text)

    # creating urls
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Sʜᴀʀᴇ URL 🔁", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

    
    
    
###### FOR CHANNEL ######


@Client.on_message((filters.document|filters.video|filters.audio|filters.photo) & filters.incoming & filters.channel & ~filters.forwarded & ~filters.edited)
async def storefile_channel(c, m):
    if IS_PRIVATE:
        if m.chat.id not in AUTH_USERS:
            return
    media = m.document or m.video or m.audio or m.photo

    # text
    text = ""
    if not m.photo:
        text = "--**🗃️ Fɪʟᴇ Dᴇᴛᴀɪʟs:**--\n\n"
        text += f"📂 ** Fɪʟᴇ ɴᴀᴍᴇ :** `{media.file_name}`\n\n" if media.file_name else ""
        text += f"🍃 **Mɪᴍᴇ Tʏᴘᴇ:** __{media.mime_type}__\n\n" if media.mime_type else ""
        text += f"📦 **Fɪʟᴇ ꜱɪᴢᴇ :** __{humanbytes(media.file_size)}__\n\n" if media.file_size else ""
        if not m.document:
            text += f"🎞 **Dᴜʀᴀᴛɪᴏɴ:** __{TimeFormatter(media.duration * 1000)}__\n\n" if media.duration else ""
            if m.audio:
                text += f"🎵 **Tɪᴛʟᴇ:** __{media.title}__\n\n" if media.title else ""
                text += f"🎙 **Pᴇʀғᴏʀᴍᴇʀ:** __{media.performer}__\n\n" if media.performer else ""
    text += f"**✏ Cᴀᴘᴛɪᴏɴ:** __{m.caption}__\n\n" if m.caption else ""
    text += f"**🍁 Uᴘʟᴏᴀᴅᴇᴅ Bʏ :--** __{m.chat.title}__\n\n"
    text += f"**🗣 Usᴇʀ Nᴀᴍᴇ:** @{m.chat.username}\n\n" if m.chat.username else ""
    text += f"**👤 Cʜᴀɴɴᴇʟ Iᴅ:** __{m.chat.id}__\n\n"
    

    # if databacase channel exist forwarding message to channel
    if DB_CHANNEL_ID:
        msg = await m.copy(int(DB_CHANNEL_ID))
        await msg.reply(text)

    # creating urls
    bot = await c.get_me()
    base64_string = await encode_string(f"{m.chat.id}_{msg.message_id}")
    url = f"https://t.me/{bot.username}?start={base64_string}"
    txt = urllib.parse.quote(text.replace('--', ''))
    share_url = f"tg://share?url={txt}File%20Link%20👉%20{url}"

    # making buttons
    buttons = [[
        InlineKeyboardButton(text="Oᴘᴇɴ Uʀʟ 🔗", url=url),
        InlineKeyboardButton(text="Sʜᴀʀᴇ Lɪɴᴋ 👤", url=share_url)
    ]]

    # Editing and adding the buttons
    await m.edit_reply_markup(InlineKeyboardMarkup(buttons))


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
        ((str(hours) + " hrs, ") if hours else "") + \
        ((str(minutes) + " min, ") if minutes else "") + \
        ((str(seconds) + " sec, ") if seconds else "") + \
        ((str(milliseconds) + " millisec, ") if milliseconds else "")
    return tmp[:-2]
