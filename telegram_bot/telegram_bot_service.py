import asyncio
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.handlers import MessageHandler
from pyrogram import Client

from database import DataBase


@dataclass(frozen=True)
class TelegramBotServiceConfig:
    app_name: str = 'telegram_bot'
    api_id: str = ''
    api_hash: Optional[str] = None
    adm_id: int = 0


default_telegram_bot_service_config = TelegramBotServiceConfig()


class TelegramBotService:
    def __init__(
        self,
        config: TelegramBotServiceConfig = default_telegram_bot_service_config,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        db: DataBase = None
    ):
        self._config = config
        self._loop = loop or asyncio.get_event_loop()

        self._client = Client("my_account", config.api_id, config.api_hash)
        self._db = db

    async def register_handlers(self):
        self._client.add_handler(MessageHandler(self._hand_mes))

    async def run_bot_task(self):
        logger.info('Bot polling started')

        await self.register_handlers()
        await self.start_sheduler()
        await self._client.start()

    async def job(self):
        users = await self._db.get_users()

        if not users:
            return

        for user in users:
            diff = (datetime.now() - user['last_date']).total_seconds() / 60

            if user['status'] == 'start' and diff >= 10:
                mes = 'Добрый день!'
                await self._client.send_message(user['tg_id'], mes)

                logger.info(
                    f'Successfully send message to {user["tg_id"]}: {mes}')

                await self._db.change_status(user['tg_id'], 'second')
            if user['status'] == 'second' and diff >= 90:
                mes = 'Подготовила для вас материал'
                photo = 'https://mimigram.ru/wp-content/uploads/2020/07/%D0%A7%D1%82%D0%BE-%D1%82%D0%B0%D0%BA%D0%BE%D0%B5-%D1%84%D0%BE%D1%82%D0%BE.jpeg'  # pylint: disable=line-too-long

                await self._client.send_message(user['tg_id'], mes)
                logger.info(
                    f'Successfully send message to {user["tg_id"]}: {mes}')

                await self._client.send_photo(user['tg_id'], photo)
                logger.info(
                    f'Successfully send photo to {user["tg_id"]}: {photo}')

                await self._db.change_status(user['tg_id'], 'last')
            if user['status'] == 'last' and diff >= 120:
                mes = 'Скоро вернусь с новым материалом!'
                await self._client.send_message(user['tg_id'], mes)

                logger.info(
                    f'Successfully send message to {user["tg_id"]}: {mes}')

                await self._db.change_status(user['tg_id'], 'start')

    async def start_sheduler(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.job, "interval", seconds=1)

        scheduler.start()

    async def _hand_mes(self, client, message):
        if message.from_user:
            print(message)
            user = await self._db.get_user(message.chat.id)

            if not user:
                await self._db.add_user(message.chat.id)
            if message.chat.id == self._config.adm_id and message.text == '/users_today':
                len_today_users = await self._db.get_users_today()

                await client.send_message(
                    'me',
                    f'Количество пользоватей, зарегестрированных сегодня: {len_today_users}'
                )
                logger.info(
                    f'Successfully send message to admin with command: {message.text}')
