# import contextlib

from base import orm

# from config import db_config
from _config import db_config

def session():
    if not orm._orm or db_config['database'] not in orm._orm:
        orm.activate_orm(db_config)

    _session = orm._orm[db_config['database']].session()

    return _session
