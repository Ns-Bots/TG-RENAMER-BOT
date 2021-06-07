import logging
logger = logging.getLogger(__name__)

import datetime
from ..config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied


@Client.on_message(filters.private & filters.incoming)
async def force_sub(c, m):
    if Config.FORCE_SUB:
        try:
            chat = await c.get_chat_member(Config.FORCE_SUB, m.from_user.id)
            if chat.status=='kicked':
                return await m.reply_text('Hai you are kicked from my updates channel. So, you are not able to use me',  quote=True)

        except UserNotParticipant:
            button = [[InlineKeyboardButton('join Updates channel', url=f'https://t.me/{Config.FORCE_SUB}')]]
            markup = InlineKeyboardMarkup(button)
            return await m.reply_text(text="Hey join in my updates channel to use me.", parse_mode='markdown', reply_markup=markup, quote=True)

        except ChatAdminRequired:
            logger.warning(f"Make me admin in @{Config.FORCE_SUB}")
            if m.from_user.id in Config.AUTH_USERS:
                return await m.reply_text(f"Make me admin in @{Config.FORCE_SUB}")

        except UsernameNotOccupied:
            logger.warning("The forcesub username was Incorrect. Please give the correct username.")
            if m.from_user.id in Config.AUTH_USERS:
                return await m.reply_text("The forcesub username was Incorrect. Please give the correct username.")

        except Exception as e:
            if "belongs to a user" in str(e):
                logger.warning("Forcesub username must be a channel username Not yours or any other users username")
                if m.from_user.id in Config.AUTH_USERS:
                    return await m.reply_text("Forcesub username must be a channel username Not yours or any other users username")
            logger.error(e)
            return await m.reply_text("Some thing went wrong. Try again and if same issue occur contact [our group](https://t.me/Ns_Bot_supporters)", disable_web_page_preview=True, quote=True)

    await m.continue_propagation()

