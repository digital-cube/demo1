# import contextlib

from base import orm, config

# from config import db_config
# from _config import db_config

def session():
    print(config.conf['db'])
    if not orm._orm or config.conf['db'] not in orm._orm:
        orm.activate_orm(config.conf['db'])

    _session = orm._orm[config.conf['db']['database']].session()

    return _session
