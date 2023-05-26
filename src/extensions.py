# -*- coding: utf-8 -*-
from contextlib import contextmanager

import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from .config import DefaultConfig as Config

Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine, autoflush=False)

# redis_cached = redis.Redis(
#     host=Config.REDIS_HOST,
#     port=Config.REDIS_PORT,
#     db=Config.REDIS_DB,
#     decode_responses=True,
#     health_check_interval=15
# )

redis_cached = redis.Redis.from_url(Config.REDIS_CACHED_URL, decode_responses=True)




@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    # except IntegrityError:
    #     session.rollback()
    #     raise
    except Exception as e:
        # logging.exception(e)
        session.rollback()
        session.close()
        raise
    finally:
        session.close()

