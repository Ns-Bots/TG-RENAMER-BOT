from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

import threading
import asyncio

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, UniqueConstraint, func


from ..config import Config


def start() -> scoped_session:
    engine = create_engine(Config.DATABASE_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class Database(BASE):
    __tablename__ = "database"
    id = Column(Integer, primary_key=True)
    thumb_id = Column(Integer)
    upload_mode = Column(Boolean)
    is_logged = Column(Boolean)

    def __init__(self, id, thumb_id, upload_mode, is_logged):
        self.id = id
        self.thumb_id = thumb_id
        self.upload_mode = upload_mode
        self.is_logged = is_logged

Database.__table__.create(checkfirst=True)

async def update_login(id, is_logged):
    with INSERTION_LOCK:
        msg = SESSION.query(Database).get(id)
        if not msg:
            msg = Database(id, None, True, False)
        else:
            msg.is_logged = is_logged
            SESSION.delete(msg)
        SESSION.add(msg)
        SESSION.commit()

async def update_mode(id, mode):
    with INSERTION_LOCK:
        msg = SESSION.query(Database).get(id)
        if not msg:
            msg = Database(id, None, True, False)
        else:
            msg.upload_mode = mode
            SESSION.delete(msg)
        SESSION.add(msg)
        SESSION.commit()

async def update_thumb(id, thumb_id):
    with INSERTION_LOCK:
        msg = SESSION.query(Database).get(id)
        if not msg:
            msg = Database(id, thumb_id, True, False)
        else:
            msg.thumb_id = thumb_id
            SESSION.delete(msg)
        SESSION.add(msg)
        SESSION.commit()

async def del_user(id):
    with INSERTION_LOCK:
        msg = SESSION.query(Database).get(id)
        if msg:
            SESSION.delete(msg)
            SESSION.commit()
            return True
        else:
            return False

async def get_data(id):
    try:
        user_data = SESSION.query(Database).get(id)
        if not user_data:
            new_user = Database(id, None, True, False)
            SESSION.add(new_user)
            SESSION.commit()
            user_data = SESSION.query(Database).get(id)
        return user_data
    finally:
        SESSION.close()
