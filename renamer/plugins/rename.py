import logging
logger = logging.getLogger(__name__)

import os
import time
import random
from ..config import Config
from ..tools.text import TEXT
from ..tools.progress_bar import progress_bar, take_screen_shot
from ..tools.timegap_check import timegap_check
from ..tools.thumbnail_fixation import fix_thumb
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from ..database.database import *
from pyrogram import Client as RenamerNs, filters
from pyrogram.errors import PeerIdInvalid, ChannelInvalid, FloodWait
from pyrogram.emoji import *


@RenamerNs.on_message((filters.document|filters.video) & filters.private & filters.incoming)
async def media(c, m):
    """Checking and Processing the renaming"""

    if Config.BANNED_USERS:
        if m.from_user.id in Config.BANNED_USERS:
            return await m.reply_text(TEXT.BANNED_USER_TEXT, quote=True)

    if Config.BOT_PASSWORD:
        is_logged = (await get_data(m.from_user.id)).is_logged
        if not is_logged and m.from_user.id not in Config.AUTH_USERS:
            return await m.reply_text(TEXT.NOT_LOGGED_TEXT, quote=True)
        
    if Config.TIME_GAP:
        time_gap = await timegap_check(m)
        if time_gap:
            return

    file_name = await c.ask(chat_id=m.from_user.id, text="Send me the New FileName for this file or send /cancel to stop", filters=filters.text)
    await file_name.delete()
    await file_name.request.delete()
    new_file_name = file_name.text
    if new_file_name.lower() == "/cancel":
        await m.delete()
        return

    if Config.TIME_GAP:
        time_gap = await timegap_check(m)
        if time_gap:
            return
        Config.TIME_GAP_STORE[m.from_user.id] = time.time()
        asyncio.get_event_loop().create_task(notify(m, Config.TIME_GAP))

    send_message = await m.reply_text(TEXT.DOWNLOAD_START)
    trace_msg = None
    if Config.TRACE_CHANNEL:
        try:
            media = await m.copy(chat_id=Config.TRACE_CHANNEL)
            trace_msg = await media.reply_text(f'**User Name:** {m.from_user.mention(style="md")}\n\n**User Id:** `{m.from_user.id}`\n\n**New File Name:** `{new_file_name}`\n\n**Status:** Downloading....')
        except PeerIdInvalid:
            logger.warning("Give the correct Channel or Group ID.")
        except ChannelInvalid:
            logger.warning("Add the bot in the Trace Channel or Group as admin to send details of the users using your bot")
        except Exception as e:
            logger.warning(e)

    download_location = f'{Config.DOWNLOAD_LOCATION}/{m.from_user.id}/'
    if not os.path.isdir(download_location):
        os.makedirs(download_location)

    start_time = time.time()
    try:
        file_location = await m.download(
                            file_name=download_location,
                            progress=progress_bar,
                            progress_args=("Downloading:", start_time, send_message)
                        )
    except Exception as e:
        logger.error(e)
        await send_message.edit(f"**Error:** {e}")
        if trace_msg:
            await trace_msg.edit(f'**User Name:** {m.from_user.mention(style="md")}\n\n**User Id:** `{m.from_user.id}`\n\n**New File Name:** `{new_file_name}`\n\n**Status:** Failed\n\nCheck logs for error')
        return

    new_file_location = f"{download_location}{new_file_name}"
    os.rename(file_location, new_file_location)

    try:
        metadata = extractMetadata(createParser(new_file_location))
        duration = 0
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
    except:
        duration = 0

    thumbnail_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    # if thumbnail not exists checking the database for thumbnail
    if not os.path.exists(thumbnail_location):
        thumb_id = (await get_data(m.from_user.id)).thumb_id

        if thumb_id:
            thumb_msg = await c.get_messages(m.chat.id, thumb_id)
            try:
                thumbnail_location = await thumb_msg.download(file_name=thumbnail_location)
            except:
                thumbnail_location = None
        else:
            try:
                thumbnail_location = await take_screen_shot(new_file_location, os.path.dirname(os.path.abspath(new_file_location)), random.randint(0, duration - 1))
            except Exception as e:
                logger.error(e)
                thumbnail_location = None

    width, height, thumbnail = await fix_thumb(thumbnail_location)

    try:
        await send_message.edit(TEXT.UPLOAD_START)
        if trace_msg:
            await trace_msg.edit(f'**User Name:** {m.from_user.mention(style="md")}\n\n**User Id:** `{m.from_user.id}`\n\n**New File Name:** `{new_file_name}`\n\n**Status:** Uploading')
    except:
        pass

    caption = str(new_file_name)
    if Config.CUSTOM_CAPTION:
        caption += f"\n\n {Config.CUSTOM_CAPTION}"
    as_file = (await get_data(m.from_user.id)).upload_mode
    if as_file:
        try:
            await m.reply_document(
                document=new_file_location,
                caption=caption,
                thumb=thumbnail,
                progress=progress_bar,
                progress_args=("Uploading:", start_time, send_message)
            )
        except FloodWait as e:
            asyncio.sleep(e.x)
            logger.warning(f"Got FloodWait for {e.x} Seconds")
        except Exception as e:
            logger.error(e)

    else:
        try:
            await m.reply_video(
                video=new_file_location,
                duration=duration,
                width=width,
                height=height,
                caption=caption,
                thumb=thumbnail,
                progress=progress_bar,
                progress_args=("Uploading:", start_time, send_message)
            )
        except FloodWait as e:
            asyncio.sleep(e.x)
            logger.warning(f"Got FloodWait for {e.x} Seconds")
        except Exception as e:
            logger.error(e)

    try:
        await send_message.edit(TEXT.UPLOAD_SUCESS, disable_web_page_preview=True)
        if trace_msg:
            await trace_msg.edit(f'**User Name:** {m.from_user.mention(style="md")}\n\n**User Id:** `{m.from_user.id}`\n\n**New File Name:** `{new_file_name}`\n\n**Status:** Uploaded Sucessfully {CHECK_MARK_BUTTON}')
        os.remove(new_file_location)
    except:
        pass

async def notify(m, time_gap):
    await asyncio.sleep(time_gap)
    await m.reply_text("__You can use me Now__")
