from aiogram.bot.api import log
import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy import sql
from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from gino import Gino

import config


db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    query: sql.select

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"
    
    @classmethod
    async def get(cls, *args, **kwargs):
        return await cls.query.where(*args, **kwargs).gino.first()
    
    @classmethod
    async def filter(cls, *args, **kwargs):
        return await cls.query.where(*args, **kwargs).gino.all()
    
    @classmethod
    async def all(cls):
        return await cls.query.gino.all()
    
    @classmethod
    async def delete(cls, *args, **kwargs):
        return await cls.query.where(*args, **kwargs).gino.delete()
    
    @classmethod
    async def new(cls, **kwargs):
        return await cls(**kwargs).create()

    @classmethod
    async def count(cls):
        return db.func.count(cls).gino.scalar()



class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
    )


async def on_startup(dispatcher: Dispatcher):
    # log.warning("!!!")
    await db.set_bind(config.DATABASE_URL)
    await db.gino.drop_all()
    await db.gino.create_all()


async def on_shutdown(dispatcher: Dispatcher):
    bind = db.pop_bind()
    if bind:
        await bind.close()


def setup(executor: Executor):
    executor.on_startup = on_startup
    executor.on_shutdown = on_shutdown
