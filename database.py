"""Модуль БД"""
from datetime import datetime


class DataBase(): # pylint: disable=missing-class-docstring
    def __init__(self, conn):
        self._conn = conn

    async def db_init(self): # pylint: disable=missing-function-docstring
        try:
            await self._conn.execute(
                'CREATE DATABASE "test_base" OWNER "postgres"'
            )
        except:# pylint: disable=bare-except
            pass
        try:
            await self._conn.execute('''
                CREATE TABLE users_data(
                    id serial PRIMARY KEY,
                    tg_id int,
                    last_date TIMESTAMP,
                    reg_date TIMESTAMP,
                    status text
                )
            ''')
        except:# pylint: disable=bare-except
            pass

    async def get_users(self): # pylint: disable=missing-function-docstring
        users = await self._conn.fetch('''
                SELECT * FROM users_data
        ''')
        return users

    async def get_user(self, tgid): # pylint: disable=missing-function-docstring
        user = await self._conn.fetch('''
                SELECT * FROM users_data WHERE tg_id = $1 
        ''', tgid)

        return user

    async def add_user(self, tgid): # pylint: disable=missing-function-docstring
        await self._conn.execute('''
            INSERT INTO users_data(tg_id, last_date, reg_date, status) VALUES($1, $2, $3, $4)
        ''', tgid, datetime.now(), datetime.now(), 'start')

    async def change_status(self, tgid, status): # pylint: disable=missing-function-docstring
        await self._conn.execute('''
            UPDATE users_data SET status = $1 WHERE tg_id = $2
            ''', status, tgid)
        await self._conn.execute('''
            UPDATE users_data SET last_date = $1 WHERE tg_id = $2
            ''', datetime.now(), tgid)

    async def get_users_today(self): # pylint: disable=missing-function-docstring
        users = await self.get_users()
        date_now = datetime.now().date()

        today_users = []

        for user in users:
            if user['reg_date'].date() == date_now:
                today_users.append(user)

        return len(today_users)
