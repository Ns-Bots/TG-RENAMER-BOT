import logging
logger = logging.getLogger(__name__)

import os
from ..config import Config
from ..tools.text import TEXT
from ..database.database import *
from pyrogram import Client as RenamerNs, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


################## Saving thumbnail 🖼 ##################

@RenamerNs.on_message(filters.photo & filters.incoming & filters.private)
async def save_photo(c, m):
    if Config.BANNED_USERS:
        if m.from_user.id in Config.BANNED_USERS:
            return await m.reply_text(TEXT.BANNED_USER_TEXT, quote=True)

    if Config.BOT_PASSWORD:
        is_logged = (await get_data(m.from_user.id)).is_logged
        if not is_logged and not Config.AUTH_USERS:
            return await m.reply_text(TEXT.NOT_LOGGED_TEXT, quote=True)

    download_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    await update_thumb(m.from_user.id, m.message_id)
    await m.download(file_name=download_location)

    await m.reply_text(
        text=TEXT.SAVED_CUSTOM_THUMBNAIL,
        quote=True
    )


################## Deleting permanent thumbnail 🗑 ##################

@RenamerNs.on_message(filters.command("deletethumbnail") & filters.incoming & filters.private)
async def delete_thumbnail(c, m):
    if Config.BANNED_USERS:
        if m.from_user.id in Config.BANNED_USERS:
            return await m.reply_text(TEXT.BANNED_USER_TEXT, quote=True)

    if Config.BOT_PASSWORD:
        is_logged = (await get_data(m.from_user.id)).is_logged
        if not is_logged and not Config.AUTH_USERS:
            return await m.reply_text(TEXT.NOT_LOGGED_TEXT, quote=True)

    download_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    thumbnail = (await get_data(m.from_user.id)).thumb_id

    if not thumbnail:
        text = TEXT.NO_CUSTOM_THUMB_NAIL_FOUND
    else:
        await update_thumb(m.from_user.id, None)
        text = TEXT.DELETED_CUSTOM_THUMBNAIL

    try:
        os.remove(download_location)
    except:
        pass

    await m.reply_text(
        text=text,
        quote=True
    )


################## Sending permanent thumbnail 🕶 ##################

@RenamerNs.on_message(filters.command("showthumbnail") & filters.incoming & filters.private)
async def show_thumbnail(c, m):
    if Config.BANNED_USERS:
        if m.from_user.id in Config.BANNED_USERS:
            return await m.reply_text(TEXT.BANNED_USER_TEXT, quote=True)

    if Config.BOT_PASSWORD:
        is_logged = (await get_data(m.from_user.id)).is_logged
        if not is_logged and not Config.AUTH_USERS:
            return await m.reply_text(TEXT.NOT_LOGGED_TEXT, quote=True)

    thumbnail = (await get_data(m.from_user.id)).thumb_id

    if not thumbnail:
         await m.reply_text(
             text=TEXT.NO_CUSTOM_THUMB_NAIL_FOUND, 
             quote=True
         )
    else:
         download_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"

         if not os.path.exists(download_location):
             thumb_nail = await c.get_messages(m.chat.id, thumbnail)
             try:
                 download_location = await thumb_nail.download(file_name=download_location)
             except:
                 await update_thumb(m.from_user.id, None)
                 return await m.reply_text(text=TEXT.NO_CUSTOM_THUMB_NAIL_FOUND, quote=True)

         await m.reply_photo(
             photo=download_location,
             caption=TEXT.THUMBNAIL_CAPTION,
             parse_mode="markdown",
             quote=True
         )


################## THE END 🛑 ##################
