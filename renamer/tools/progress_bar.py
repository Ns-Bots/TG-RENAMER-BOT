import logging
logger = logging.getLogger(__name__)

import os
import math
import time
import asyncio
from ..config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.emoji import *

############################# Progress Bar 📊 #############################

async def progress_bar(current, total, status_msg, start, msg):
    present = time.time()
    if round((present - start) % 3) == 0 or current == total:
        speed = current / (present - start)
        percentage = current * 100 / total
        time_to_complete = round(((total - current) / speed)) * 1000
        time_to_complete = TimeFormatter(time_to_complete)
        progressbar = "[{0}{1}]".format(\
            ''.join([f"{BLACK_MEDIUM_SMALL_SQUARE}" for i in range(math.floor(percentage / 10))]),
            ''.join([f"{WHITE_MEDIUM_SMALL_SQUARE}" for i in range(10 - math.floor(percentage / 10))])
            )
        current_message = f"""**{status_msg}** {round(percentage, 2)}%
{progressbar}

{HOLLOW_RED_CIRCLE} **Speed**: {humanbytes(speed)}/s

{HOLLOW_RED_CIRCLE} **Done**: {humanbytes(current)}

{HOLLOW_RED_CIRCLE} **Size**: {humanbytes(total)}

{HOLLOW_RED_CIRCLE} **Time Left**: {time_to_complete}"""
        try:
            await msg.edit(text=current_message)
        except:
            pass


############################# Size #############################

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


############################# Time Formating ⏰ #############################

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
        ((str(hours) + " hours, ") if hours else "") + \
        ((str(minutes) + " min, ") if minutes else "") + \
        ((str(seconds) + " sec, ") if seconds else "") + \
        ((str(milliseconds) + " millisec, ") if milliseconds else "")
    return tmp[:-2]


############################# Taking Screenshots 📸 #############################

async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None

############################# END 🌋 #############################
