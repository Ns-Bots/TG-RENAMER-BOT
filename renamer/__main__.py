import logging

# Get logging configurations
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - Line: %(lineno)d - Path: %(name)s - Module: %(module)s.py - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.WARNING)

import os
from .config import Config
from pyrogram import Client
from pyromod import listen


def main():

    Renamer = Client("Renamer_NsBot",
                 bot_token=Config.BOT_TOKEN,
                 api_id=Config.API_ID,
                 api_hash=Config.API_HASH,
                 plugins=dict(root="renamer/plugins"),
                 workers=100)

    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    Renamer.run()


if __name__ == "__main__":
    main()



