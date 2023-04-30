import click


@click.group()
def cli():
    from bot import misc

    misc.setup()


@cli.command()
def polling():
    """
    Start application in polling mode
    """

    from aiogram import executor
    #from aiogram.utils.executor import Executor

    from bot.misc import dp
    from . import db

    #executor = Executor(dp)

    #db.setup(executor)

    executor.skip_updates = True

    executor.start_polling(dp, on_startup=db.on_startup)
