import sqlalchemy as sa

from bot.utils.db import db

from .. import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = sa.Column(sa.BigInteger, primary_key=True)
    username = sa.Column(sa.String(50), unique=True)
