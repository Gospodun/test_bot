"""Запуск процессов логирования, БД и бота"""
import asyncio
import asyncpg
from loguru import logger

from database import DataBase
from config import Config
from telegram_bot import TelegramBotService


async def main(config: Config, loop: asyncio.AbstractEventLoop): # pylint: disable=missing-function-docstring
    logger.add('logs/logs.log', level='DEBUG')
    logger.info(f'{config.app_name} started')
    logger.info(f'PostgreSQL connection {config.pg_connection}', config.pg_connection)

    conn = await asyncpg.connect(config.pg_connection)
    db = DataBase(conn=conn)
    await db.db_init()

    telegram_bot_service = TelegramBotService(
        config=config.telegram_bot_service_config,
        loop=loop,
        db=db
    )

    loop.create_task(telegram_bot_service.run_bot_task())
