import logging

# Get logging configurations
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - Line: %(lineno)d - Path: %(name)s - Module: %(module)s.py - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.WARNING)

import platform
from .plugins import *
from .config import Config
from pyrogram import Client, __version__, idle
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyromod import listen


def main():

    Renamer = Client("Renamer_NsBot",
                 bot_token=Config.BOT_TOKEN,
                 api_id=Config.API_ID,
                 api_hash=Config.API_HASH,
                 plugins=dict(root="renamer/plugins"),
                 workers=100)

    Renamer.start()
    me = Renamer.get_me()

    Renamer.add_handler(MessageHandler(
        media,
        filters=filters.command(['rename', f'rename@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        help,
        filters=filters.command(['help', f'help@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        about,
        filters=filters.command(['about', f'about@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        start,
        filters=filters.command(['start', f'start@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        set_mode,
        filters=filters.command(['mode', f'mode@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        reset_user,
        filters=filters.command(['reset', f'reset@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        password,
        filters=filters.command(['login', f'login@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        save_photo,
        filters=filters.command(['savethumbnail', f'savethumbnail@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        delete_thumbnail,
        filters=filters.command(['deletethumbnail', f'deletethumbnail@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    Renamer.add_handler(MessageHandler(
        show_thumbnail,
        filters=filters.command(['showthumbnail', f'showthumbnail@{me.username}'])
        & filters.chat(chats=Config.AUTH_GROUP),
    ))

    startup_msg = f"Successfully deployed your Renamer at @{me.username}\n"
    startup_msg += f"Pyrogram Version: V{__version__}\n"
    startup_msg += f"Python Version: V{platform.python_version()}\n\n"
    startup_msg += "Thanks for deploying our bot. Please give a star to my repo and join @Ns_bot_updates."
    print(startup_msg)

    idle()

    Renamer.stop()
    print("Ok bye bye 😢.")

if __name__ == "__main__":
    main()



