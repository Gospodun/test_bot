"""Конфиг бота"""
import os
from dataclasses import dataclass
import toml

from telegram_bot import TelegramBotServiceConfig, default_telegram_bot_service_config


app_root = os.path.abspath(os.path.dirname(__file__))
pyproject_info = toml.load(os.path.join(app_root, 'pyproject.toml'))
poetry_info = pyproject_info['tool']['poetry']

app_name = poetry_info['name']
app_version = poetry_info['version']


@dataclass(frozen=True)
class Config:  # pylint: disable=missing-class-docstring
    pg_connection: str

    telegram_bot_service_config: TelegramBotServiceConfig = default_telegram_bot_service_config

    app_name: str = app_name
    app_version: str = app_version

    telegram_api_id: int = None
    telegram_api_hash: str = None
    telegram_adm_id: int = None
