import logging
import json
import os
import sys
sys.path.append(os.getcwd())  # NOQA

import discord
from discord.ext import commands

import requests
from dotenv import load_dotenv
from PIL import Image
from datetime import datetime as dt

# Load the environment variables
load_dotenv(override=True)

# Init the logger
log_format = '%(asctime)s - [%(levelname)s] - %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger('download_bot')
file_handler = logging.FileHandler(filename='logs/download_bot.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
logger.addHandler(file_handler)

# Stream the logs to the console with color and format
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# Record the logs of discord as well
discord_logger = logging.getLogger('discord')
discord_file_handler = logging.FileHandler(filename='logs/download_bot.log', encoding='utf-8')
discord_file_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
discord_logger.addHandler(discord_file_handler)

# Stream the logs of discord as well
discord_stream_handler = logging.StreamHandler()
discord_stream_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
discord_logger.addHandler(discord_stream_handler)

logger.setLevel(logging.INFO)
discord_logger.setLevel(logging.INFO)


class DownloadBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="*", intents=discord.Intents.all())
        self.discord_token = os.getenv('DOWNLOAD_BOT_TOKEN')

        # Read the configs
        self._read_configs()

    def _read_configs(self):
        with open('configs/images.json', 'r', encoding='utf-8') as f:
            self.images_configs = json.load(f)

        logger.info('Configs read successfully')

    def _split_image(self, image_file_path: str):
        with Image.open(image_file_path) as img:
            width, height = img.size

            mid_x = width // 2
            mid_y = height // 2

            top_left = img.crop((0, 0, mid_x, mid_y))
            top_right = img.crop((mid_x, 0, width, mid_y))
            bottom_left = img.crop((0, mid_y, mid_x, height))
            bottom_right = img.crop((mid_x, mid_y, width, height))

            return top_left, top_right, bottom_left, bottom_right

    async def _download_image(self, url, file_name):
        response = requests.get(url)
        if response.status_code == 200:
            date_today = dt.now().strftime('%Y-%m-%d')

            # Create the folder to store the original images
            os.makedirs(f'download/{date_today}/original', exist_ok=True)

            with open(f'download/{date_today}/original/{file_name}', 'wb') as f:
                f.write(response.content)
            logger.info(f'Downloaded successfully to "{date_today}": "{file_name}"')

            if "UPSCALED_" in file_name:
                logger.warning(f'Images {file_name} are already upscaled !')

            # Split the image if the setting is enabled
            if self.images_configs['split_images']:
                top_left, top_right, bottom_left, bottom_right = self._split_image(
                    f'download/{date_today}/original/{file_name}')

                ext = file_name.split('.')[-1]
                just_name = file_name.replace(f'.{ext}', '')

                # Create the folder to store the split images
                save_dir = f'download/{date_today}/split/{just_name}'
                os.makedirs(save_dir, exist_ok=True)

                top_left.save(os.path.join(save_dir, f'{just_name}_top_left.{ext}'))
                top_right.save(os.path.join(save_dir, f'{just_name}_top_right.{ext}'))
                bottom_left.save(os.path.join(save_dir, f'{just_name}_bottom_left.{ext}'))
                bottom_right.save(os.path.join(save_dir, f'{just_name}_bottom_right.{ext}'))

                logger.info(f'Split successfully to "{date_today}": "{file_name}"')

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Download images bot is ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        logger.info(f'Message received from {message.author.name}')

        for attachment in message.attachments:
            if "Upscaled by" in message.content:
                file_prefix = 'UPSCALED_'
            else:
                file_prefix = ''

            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                await self._download_image(attachment.url, f"{file_prefix}{attachment.filename}")

                # Send the message to the channel
                await message.channel.send(f"Downloaded successfully: {attachment.filename}")
                logger.info(f"Downloaded successfully: {attachment.filename}")


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')
    client = DownloadBot()
    client.run(os.getenv('DOWNLOAD_BOT_TOKEN'), reconnect=True)
