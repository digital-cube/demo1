# import contextlib

from base import orm, config

# from config import db_config
# from _config import db_config

def session():
    if not orm._orm or config.conf['db']['database'] not in orm._orm:
        dbc = config.conf['db']
        orm.activate_orm(dbc)

    _session = orm._orm[config.conf['db']['database']].session()

    return _session
