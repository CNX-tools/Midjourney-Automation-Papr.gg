import json
import logging
import os
import sys
import pyautogui as pg
sys.path.append(os.getcwd())  # NOQA

import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

from utils.window_interaction import _minimize_window

load_dotenv()

# Init the logger
log_format = '%(asctime)s - [%(levelname)s] - %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger('prompt_bot')
file_handler = logging.FileHandler(filename='logs/prompt_bot.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
logger.addHandler(file_handler)

# Stream the logs to the console with color and format
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# Record the logs of discord as well
discord_logger = logging.getLogger('discord')
discord_file_handler = logging.FileHandler(filename='logs/prompt_bot.log', encoding='utf-8')
discord_file_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
discord_logger.addHandler(discord_file_handler)

# Stream the logs of discord as well
discord_stream_handler = logging.StreamHandler()
discord_stream_handler.setFormatter(logging.Formatter(log_format, datefmt=datefmt))
discord_logger.addHandler(discord_stream_handler)

logger.setLevel(logging.INFO)
discord_logger.setLevel(logging.INFO)


class PromptBot(commands.Bot):
    def __init__(self, prompts_file_path: str) -> None:
        super().__init__(command_prefix="*", intents=discord.Intents.all())
        self.discord_token = os.getenv('PROMPT_BOT_TOKEN')
        self._read_configs()
        self._read_prompts(prompts_file_path)
        self.prompt_counter = 0

    def _read_configs(self):
        with open('configs/general.json', 'r', encoding='utf-8') as f:
            self.general_configs = json.load(f)

        with open('configs/images.json', 'r', encoding='utf-8') as f:
            self.images_configs = json.load(f)

        with open('configs/prompts.json', 'r', encoding='utf-8') as f:
            self.prompts_configs = json.load(f)

        logger.info('Configs read successfully')

    def _read_prompts(self, prompts_file_path: str):
        with open(prompts_file_path, 'r', encoding='utf-8') as f:
            self.prompts: list = list(map(lambda x: x.strip(), f.readlines()))

        self.prompts = list(filter(lambda x: x != '', self.prompts))

        for i, prompt in enumerate(self.prompts):
            logger.info(f'Prompt {i + 1}: {prompt}')
        logger.info(f'Prompts read successfully. Founded {len(self.prompts)} prompts')

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Prompt bot connected')

    @commands.Cog.listener()
    async def on_message(self, message):
        logger.info(f'New message received from {message.author.name}')

        msg = message.content

        if msg == self.general_configs['start_command']:
            while True:
                if self.prompt_counter >= len(self.prompts):
                    await message.channel.send('All prompts have been entered successfully !')
                    _minimize_window('#general | Bot Generator Server - Discord')
                    sys.exit(0)

                logger.info(f'Starting entering the prompts...')
                await asyncio.sleep(2)
                pg.write('/')
                # await asyncio.sleep(0.5)
                pg.write('im')
                await asyncio.sleep(0.5)
                pg.press('tab')
                await asyncio.sleep(0.5)
                prompt = f"{self.prompts_configs['prefix']} {self.prompts[self.prompt_counter]} {self.prompts_configs['suffix']}"
                logger.info(f'Entering the prompts: {prompt}')
                pg.write(prompt)
                await asyncio.sleep(0.5)
                pg.press('enter')
                await asyncio.sleep(0.5)
                self.prompt_counter += 1


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if os.path.exists('.temp/temp_prompt.txt'):
        bot = PromptBot('.temp/temp_prompt.txt')
        bot.run(bot.discord_token)
