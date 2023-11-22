"Запуск бота и получение конфига"
import asyncio
import signal
from typing import Dict

import click

import app
from config import Config, app_name
from telegram_bot import TelegramBotServiceConfig


def stop_loop(loop: asyncio.AbstractEventLoop):
    loop.stop()


def exception_handler(loop: asyncio.AbstractEventLoop, context: Dict):
    loop.default_exception_handler(context)
    stop_loop(loop)


@click.command()
@click.argument('telegram_api_id', envvar='TELEGRAM_API_ID', type=str)  # noqa
@click.argument('telegram_adm_id', envvar='TELEGRAM_ADM_ID', type=int)  # noqa
@click.argument('telegram_api_hash', envvar='TELEGRAM_API_HASH', type=str)  # noqa
@click.argument('pg_connection', envvar='PG_CONNECTION', type=str)  # noqa
def main(  # pylint: disable=too-many-arguments
    telegram_api_id: str,
    telegram_adm_id: int,
    telegram_api_hash: str,
    pg_connection: str
):
    config = Config(
        pg_connection=pg_connection,
        telegram_bot_service_config=TelegramBotServiceConfig(
            app_name=app_name,
            api_id=telegram_api_id,
            api_hash=telegram_api_hash,
            adm_id=telegram_adm_id
        ),
    )

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)
    for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop_loop, loop)

    loop.create_task(app.main(config, loop))
    loop.run_forever()


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
